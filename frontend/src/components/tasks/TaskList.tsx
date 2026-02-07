// [Task T040] Task list component - Enhanced with filters and categories
'use client';

import { useEffect, useState, forwardRef, useImperativeHandle } from 'react';
import { Task } from '@/lib/types/task';
import { Category } from '@/lib/types/category';
import { tasksApi } from '@/lib/api/tasks';
import { categoriesApi } from '@/lib/api/categories';
import TaskItem from './TaskItem';

interface Props {
  searchQuery?: string;
  priorityFilter?: string;
  statusFilter?: string;
}

const TaskList = forwardRef<any, Props>(({ searchQuery, priorityFilter, statusFilter }, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError('');

      // Build filter object
      const filters: any = {};
      if (priorityFilter) filters.priority = priorityFilter;
      if (statusFilter === 'completed') filters.completed = true;
      if (statusFilter === 'active') filters.completed = false;
      if (searchQuery) filters.search = searchQuery;

      const data = await tasksApi.getAll(filters);
      setTasks(data);
    } catch (err) {
      console.error('Failed to load tasks:', err);
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const data = await categoriesApi.getAll();
      setCategories(data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  // Expose loadTasks to parent via ref
  useImperativeHandle(ref, () => ({
    loadTasks
  }));

  useEffect(() => {
    loadTasks();
    loadCategories();
  }, []);

  useEffect(() => {
    loadTasks();
  }, [searchQuery, priorityFilter, statusFilter]);

  const handleTaskUpdated = () => {
    loadTasks();
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
        <div className="flex flex-col items-center justify-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <div className="text-gray-500 dark:text-gray-400 font-medium">Loading tasks...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/30 border-2 border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-6 py-4 rounded-xl shadow-sm">
        <div className="flex items-center">
          <svg className="h-5 w-5 text-red-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="font-medium">Error: {error}</span>
        </div>
        <button
          onClick={loadTasks}
          className="mt-3 text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 underline"
        >
          Try again
        </button>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12">
        <div className="text-center">
          <div className="mx-auto h-24 w-24 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mb-4">
            <svg className="h-12 w-12 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            No tasks found
          </h3>
          <p className="text-gray-500 dark:text-gray-400">
            {searchQuery || priorityFilter || statusFilter
              ? 'Try adjusting your filters'
              : 'Create your first task to get started!'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onTaskUpdated={handleTaskUpdated}
          categories={categories}
        />
      ))}
    </div>
  );
});

TaskList.displayName = 'TaskList';

export default TaskList;
