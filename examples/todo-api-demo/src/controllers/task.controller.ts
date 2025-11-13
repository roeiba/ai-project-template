/**
 * Task Controller
 *
 * Handles HTTP requests for task management operations
 * Implements business logic defined in PROJECT_BRIEF.md
 */

import { Request, Response, NextFunction } from 'express';
import { TaskService } from '../services/task.service';
import { CreateTaskDTO, UpdateTaskDTO, TaskFilterOptions } from '../models/Task';
import { AuthRequest } from '../middleware/auth';
import { logger } from '../utils/logger';

export class TaskController {
  private taskService: TaskService;

  constructor() {
    this.taskService = new TaskService();
  }

  /**
   * Create a new task
   * POST /api/v1/tasks
   */
  createTask = async (req: AuthRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.user!.id;
      const taskData: CreateTaskDTO = req.body;

      const task = await this.taskService.createTask(userId, taskData);

      logger.info(`Task created: ${task.id} by user: ${userId}`);

      res.status(201).json({
        success: true,
        data: task,
        message: 'Task created successfully'
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * Get all tasks for the authenticated user
   * GET /api/v1/tasks
   */
  getTasks = async (req: AuthRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.user!.id;
      const filters: TaskFilterOptions = {
        status: req.query.status as any,
        priority: req.query.priority as any,
        listId: req.query.listId as string,
        search: req.query.search as string
      };

      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 20;

      const result = await this.taskService.getTasks(userId, filters, page, limit);

      res.status(200).json({
        success: true,
        data: result.tasks,
        pagination: {
          page,
          limit,
          total: result.total,
          totalPages: Math.ceil(result.total / limit)
        }
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * Get a single task by ID
   * GET /api/v1/tasks/:id
   */
  getTaskById = async (req: AuthRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.user!.id;
      const taskId = req.params.id;

      const task = await this.taskService.getTaskById(taskId, userId);

      if (!task) {
        res.status(404).json({
          success: false,
          message: 'Task not found'
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: task
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * Update a task
   * PATCH /api/v1/tasks/:id
   */
  updateTask = async (req: AuthRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.user!.id;
      const taskId = req.params.id;
      const updates: UpdateTaskDTO = req.body;

      const task = await this.taskService.updateTask(taskId, userId, updates);

      logger.info(`Task updated: ${taskId} by user: ${userId}`);

      res.status(200).json({
        success: true,
        data: task,
        message: 'Task updated successfully'
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * Delete a task
   * DELETE /api/v1/tasks/:id
   */
  deleteTask = async (req: AuthRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.user!.id;
      const taskId = req.params.id;

      await this.taskService.deleteTask(taskId, userId);

      logger.info(`Task deleted: ${taskId} by user: ${userId}`);

      res.status(200).json({
        success: true,
        message: 'Task deleted successfully'
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * Bulk update tasks
   * PATCH /api/v1/tasks/bulk
   */
  bulkUpdateTasks = async (req: AuthRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = req.user!.id;
      const { taskIds, updates } = req.body;

      const result = await this.taskService.bulkUpdateTasks(taskIds, userId, updates);

      logger.info(`Bulk update: ${result.updated} tasks by user: ${userId}`);

      res.status(200).json({
        success: true,
        data: result,
        message: `${result.updated} tasks updated successfully`
      });
    } catch (error) {
      next(error);
    }
  };
}
