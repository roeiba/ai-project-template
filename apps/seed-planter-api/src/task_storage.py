"""Task storage service using Redis for tracking async operations"""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import redis.asyncio as redis

from config import config
from models import ProjectStatus, ProjectDetails, ProjectProgress

logger = logging.getLogger(__name__)


class TaskStorage:
    """Manages task state in Redis"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.task_ttl = 3600  # Tasks expire after 1 hour
    
    async def connect(self):
        """Connect to Redis"""
        if not self.redis_client:
            self.redis_client = await redis.from_url(
                config.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info(f"Connected to Redis at {config.redis_url}")
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")
    
    def _task_key(self, task_id: str) -> str:
        """Generate Redis key for task"""
        return f"task:{task_id}"
    
    def _progress_key(self, task_id: str) -> str:
        """Generate Redis key for task progress"""
        return f"task:{task_id}:progress"
    
    async def create_task(self, task_id: str, initial_data: Dict[str, Any]) -> None:
        """Create a new task"""
        await self.connect()
        
        task_data = {
            "task_id": task_id,
            "status": ProjectStatus.INITIALIZING.value,
            "created_at": datetime.utcnow().isoformat(),
            **initial_data
        }
        
        await self.redis_client.setex(
            self._task_key(task_id),
            self.task_ttl,
            json.dumps(task_data)
        )
        
        logger.info(f"Created task {task_id}")
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: ProjectStatus,
        **kwargs
    ) -> None:
        """Update task status and additional fields"""
        await self.connect()
        
        task_key = self._task_key(task_id)
        task_data_str = await self.redis_client.get(task_key)
        
        if not task_data_str:
            logger.warning(f"Task {task_id} not found")
            return
        
        task_data = json.loads(task_data_str)
        task_data["status"] = status.value
        task_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update additional fields
        for key, value in kwargs.items():
            task_data[key] = value
        
        await self.redis_client.setex(
            task_key,
            self.task_ttl,
            json.dumps(task_data)
        )
        
        logger.debug(f"Updated task {task_id} status to {status.value}")
    
    async def update_progress(
        self,
        task_id: str,
        progress: ProjectProgress
    ) -> None:
        """Update task progress"""
        await self.connect()
        
        progress_data = {
            "task_id": task_id,
            "status": progress.status.value,
            "message": progress.message,
            "progress_percent": progress.progress_percent,
            "timestamp": progress.timestamp.isoformat(),
            "org_url": progress.org_url,
            "repo_url": progress.repo_url,
            "deployment_url": progress.deployment_url,
            "gcp_project_id": progress.gcp_project_id,
        }
        
        # Store latest progress
        await self.redis_client.setex(
            self._progress_key(task_id),
            self.task_ttl,
            json.dumps(progress_data)
        )
        
        # Also update main task status
        await self.update_task_status(
            task_id,
            progress.status,
            message=progress.message,
            progress_percent=progress.progress_percent
        )
    
    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task data"""
        await self.connect()
        
        task_data_str = await self.redis_client.get(self._task_key(task_id))
        
        if not task_data_str:
            return None
        
        return json.loads(task_data_str)
    
    async def get_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get latest progress for a task"""
        await self.connect()
        
        progress_data_str = await self.redis_client.get(self._progress_key(task_id))
        
        if not progress_data_str:
            return None
        
        return json.loads(progress_data_str)
    
    async def complete_task(
        self,
        task_id: str,
        result: ProjectDetails
    ) -> None:
        """Mark task as completed with result"""
        await self.connect()
        
        await self.update_task_status(
            task_id,
            ProjectStatus.COMPLETED,
            project_id=result.project_id,
            project_name=result.project_name,
            org_url=result.org_url,
            repo_url=result.repo_url,
            deployment_url=result.deployment_url,
            gcp_project_id=result.gcp_project_id,
            completed_at=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Task {task_id} completed successfully")
    
    async def fail_task(
        self,
        task_id: str,
        error_message: str
    ) -> None:
        """Mark task as failed"""
        await self.connect()
        
        await self.update_task_status(
            task_id,
            ProjectStatus.FAILED,
            error_message=error_message,
            failed_at=datetime.utcnow().isoformat()
        )
        
        logger.error(f"Task {task_id} failed: {error_message}")


# Global instance
task_storage = TaskStorage()
