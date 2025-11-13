#!/usr/bin/env python3
"""
Sample code file for e2e testing
This file is used to test code review, documentation generation, and fix suggestions
"""

import logging
from typing import Optional, Dict, Any


class DataProcessor:
    """Process data with validation and transformation"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data processor

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data

        Args:
            data: Input data dictionary

        Returns:
            Processed data dictionary
        """
        self.logger.info(f"Processing data: {data}")

        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")

        # Transform data
        result = {
            "status": "processed",
            "data": self._transform(data),
            "timestamp": self._get_timestamp()
        }

        return result

    def _transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform data

        Args:
            data: Input data

        Returns:
            Transformed data
        """
        # Simple transformation: convert all string values to uppercase
        transformed = {}
        for key, value in data.items():
            if isinstance(value, str):
                transformed[key] = value.upper()
            else:
                transformed[key] = value

        return transformed

    def _get_timestamp(self) -> str:
        """
        Get current timestamp

        Returns:
            ISO format timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main entry point for testing"""
    processor = DataProcessor()

    test_data = {
        "name": "test",
        "value": "sample",
        "count": 42
    }

    result = processor.process(test_data)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
