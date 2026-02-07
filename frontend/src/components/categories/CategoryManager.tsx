'use client';

import { useState, useEffect } from 'react';
import { categoriesApi } from '@/lib/api/categories';
import { Category } from '@/lib/types/category';
import toast from 'react-hot-toast';

interface Props {
  onClose: () => void;
  onCategoriesChanged: () => void;
}

export default function CategoryManager({ onClose, onCategoriesChanged }: Props) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newName, setNewName] = useState('');
  const [newColor, setNewColor] = useState('#3B82F6');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await categoriesApi.getAll();
      setCategories(data);
    } catch (err) {
      console.error('Failed to load categories:', err);
      toast.error('Failed to load categories');
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;

    setIsLoading(true);
    try {
      await categoriesApi.create({ name: newName, color: newColor });
      setNewName('');
      setNewColor('#3B82F6');
      await loadCategories();
      onCategoriesChanged();
      toast.success('Category created!');
    } catch (err) {
      console.error('Failed to create category:', err);
      toast.error('Failed to create category');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this category? Tasks will not be deleted.')) return;

    try {
      await categoriesApi.delete(id);
      await loadCategories();
      onCategoriesChanged();
      toast.success('Category deleted');
    } catch (err) {
      console.error('Failed to delete category:', err);
      toast.error('Failed to delete category');
    }
  };

  const presetColors = [
    '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
    '#EC4899', '#06B6D4', '#6366F1', '#84CC16', '#F97316'
  ];

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 dark:bg-gray-900 dark:bg-opacity-70 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Manage Categories</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-2xl">
            ×
          </button>
        </div>

        {/* Create Form */}
        <form onSubmit={handleCreate} className="mb-6 space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              New Category Name
            </label>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="e.g., Work, Personal, Shopping"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Color
            </label>
            <div className="flex gap-2 flex-wrap">
              {presetColors.map(color => (
                <button
                  key={color}
                  type="button"
                  onClick={() => setNewColor(color)}
                  className={`w-8 h-8 rounded-full border-2 ${newColor === color ? 'border-gray-900 dark:border-white' : 'border-transparent'}`}
                  style={{ backgroundColor: color }}
                  title={color}
                />
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading || !newName.trim()}
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {isLoading ? 'Creating...' : 'Create Category'}
          </button>
        </form>

        {/* Categories List */}
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Your Categories</h3>
          {categories.length === 0 ? (
            <p className="text-sm text-gray-500 dark:text-gray-400">No categories yet. Create one above!</p>
          ) : (
            categories.map(cat => (
              <div
                key={cat.id}
                className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-md"
              >
                <div className="flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: cat.color }}
                  />
                  <span className="text-sm font-medium text-gray-900 dark:text-white">{cat.name}</span>
                </div>
                <button
                  onClick={() => handleDelete(cat.id)}
                  className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 text-sm"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>

        <div className="mt-6">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
