// [Task T041, T053] Task item component - Enhanced with Priority, Due Date, Category, Tags
'use client';

import { useState } from 'react';
import { Task } from '@/lib/types/task';
import { tasksApi } from '@/lib/api/tasks';
import EditTaskForm from './EditTaskForm';
import { format, isPast, isToday } from 'date-fns';

interface Props {
  task: Task;
  onTaskUpdated: () => void;
  categories?: { id: number; name: string; color: string }[];
}

export default function TaskItem({ task, onTaskUpdated, categories = [] }: Props) {
  const [isEditing, setIsEditing] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const handleToggleComplete = async () => {
    if (isToggling) return;
    setIsToggling(true);
    try {
      await tasksApi.toggleCompletion(task.id);
      onTaskUpdated();
    } catch (err) {
      console.error('Failed to toggle task:', err);
      alert('Failed to update task. Please try again.');
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }
    try {
      await tasksApi.delete(task.id);
      onTaskUpdated();
    } catch (err) {
      console.error('Failed to delete task:', err);
      alert('Failed to delete task. Please try again.');
    }
  };

  const handleEditComplete = () => {
    setIsEditing(false);
    onTaskUpdated();
  };

  // Priority badge styling
  const priorityColors = {
    high: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    low: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  };

  // Due date styling
  const getDueDateColor = () => {
    if (!task.due_date) return '';
    const dueDate = new Date(task.due_date);
    if (isPast(dueDate) && !task.completed) {
      return 'text-red-600 dark:text-red-400 font-semibold';
    }
    if (isToday(dueDate)) {
      return 'text-orange-600 dark:text-orange-400 font-medium';
    }
    return 'text-gray-600 dark:text-gray-400';
  };

  // Parse tags
  const tags = task.tags ? JSON.parse(task.tags) : [];
  const category = categories.find(c => c.id === task.category_id);

  const truncatedDescription = task.description
    ? task.description.length > 100
      ? task.description.substring(0, 100) + '...'
      : task.description
    : '';

  return (
    <>
      <div className="bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3 flex-1">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              disabled={isToggling}
              className="mt-1 h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded cursor-pointer disabled:opacity-50"
              title={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
            />

            <div className="flex-1">
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className={`text-lg font-medium transition-all ${
                  task.completed
                    ? 'line-through text-gray-500 dark:text-gray-400'
                    : 'text-gray-900 dark:text-white'
                }`}>
                  {task.title}
                </h3>

                {/* Priority Badge */}
                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${priorityColors[task.priority]}`}>
                  {task.priority === 'high' && '🔴'} {task.priority === 'medium' && '🟡'} {task.priority === 'low' && '🟢'} {task.priority.toUpperCase()}
                </span>

                {/* Category Badge */}
                {category && (
                  <span
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-white"
                    style={{ backgroundColor: category.color }}
                  >
                    {category.name}
                  </span>
                )}
              </div>

              {task.description && (
                <p className={`mt-1 text-sm ${
                  task.completed ? 'text-gray-400 dark:text-gray-500' : 'text-gray-600 dark:text-gray-300'
                }`}>
                  {truncatedDescription}
                </p>
              )}

              {/* Tags */}
              {tags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {tags.map((tag: string, idx: number) => (
                    <span
                      key={idx}
                      className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              <div className="mt-2 flex items-center gap-4 text-xs text-gray-400 dark:text-gray-500 flex-wrap">
                <span>
                  Created: {format(new Date(task.created_at), 'MMM d, yyyy')}
                </span>

                {/* Due Date */}
                {task.due_date && (
                  <span className={getDueDateColor()}>
                    Due: {format(new Date(task.due_date), 'MMM d, yyyy h:mm a')}
                    {isPast(new Date(task.due_date)) && !task.completed && ' (Overdue!)'}
                  </span>
                )}

                {task.completed && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400">
                    ✓ Completed
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-2 ml-4">
            <button
              onClick={() => setIsEditing(true)}
              className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium"
              title="Edit task"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 text-sm font-medium"
              title="Delete task"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      {isEditing && (
        <EditTaskForm
          task={task}
          onClose={() => setIsEditing(false)}
          onTaskUpdated={handleEditComplete}
        />
      )}
    </>
  );
}
