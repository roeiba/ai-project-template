/**
 * Task Model
 *
 * Represents a task in the task management system
 * Generated based on data model specification in PROJECT_BRIEF.md
 */

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export enum TaskStatus {
  TODO = 'todo',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  ARCHIVED = 'archived'
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: TaskPriority;
  status: TaskStatus;
  dueDate?: Date;
  userId: string;
  listId?: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateTaskDTO {
  title: string;
  description?: string;
  priority?: TaskPriority;
  status?: TaskStatus;
  dueDate?: Date;
  listId?: string;
  tags?: string[];
}

export interface UpdateTaskDTO {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  status?: TaskStatus;
  dueDate?: Date;
  listId?: string;
  tags?: string[];
}

export interface TaskFilterOptions {
  status?: TaskStatus;
  priority?: TaskPriority;
  listId?: string;
  tags?: string[];
  dueBefore?: Date;
  dueAfter?: Date;
  search?: string;
}

/**
 * Task validation rules
 */
export const TaskValidation = {
  title: {
    minLength: 1,
    maxLength: 255,
    required: true
  },
  description: {
    maxLength: 5000,
    required: false
  },
  tags: {
    maxCount: 10,
    maxLength: 50
  }
};
