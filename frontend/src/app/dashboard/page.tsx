// [Task T042] Dashboard page - Enhanced with Stats, Theme Toggle, Categories
'use client';

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth/hooks';
import { useTheme } from '@/lib/contexts/ThemeContext';
import TaskList from '@/components/tasks/TaskList';
import CreateTaskForm from '@/components/tasks/CreateTaskForm';
import CategoryManager from '@/components/categories/CategoryManager';
import StatsCards from '@/components/dashboard/StatsCards';
import UserProfile from '@/components/profile/UserProfile';
import { MdDarkMode, MdLightMode, MdCategory, MdAccountCircle } from 'react-icons/md';
import { Toaster } from 'react-hot-toast';

export default function DashboardPage() {
  const router = useRouter();
  const { logout, user } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [isCreating, setIsCreating] = useState(false);
  const [isManagingCategories, setIsManagingCategories] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const taskListRef = useRef<any>(null);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const handleTaskCreated = () => {
    setIsCreating(false);
    if (taskListRef.current?.loadTasks) {
      taskListRef.current.loadTasks();
    }
  };

  const handleCategoriesChanged = () => {
    if (taskListRef.current?.loadTasks) {
      taskListRef.current.loadTasks();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      <Toaster position="top-right" />

      {/* Beautiful Header Navbar */}
      <nav className="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            <div className="flex items-center space-x-4">
              {/* Logo/Icon */}
              <div className="flex-shrink-0 flex items-center">
                <div className="h-12 w-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                  <svg className="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
              </div>
              {/* Title and Subtitle */}
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">My Todo Dashboard</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">Organize your tasks efficiently</p>
              </div>
            </div>

            {/* Right side - Actions and User */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
                title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              >
                {theme === 'light' ? <MdDarkMode size={24} /> : <MdLightMode size={24} />}
              </button>

              {/* Categories Button */}
              <button
                onClick={() => setIsManagingCategories(true)}
                className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
                title="Manage categories"
              >
                <MdCategory size={24} />
              </button>

              {/* Profile Button */}
              <button
                onClick={() => setShowProfile(true)}
                className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
                title="View profile"
              >
                <MdAccountCircle size={24} />
              </button>

              {/* User badge */}
              {user?.email && (
                <button
                  onClick={() => setShowProfile(true)}
                  className="hidden sm:flex items-center space-x-2 bg-indigo-50 dark:bg-indigo-900/30 px-4 py-2 rounded-lg hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition cursor-pointer"
                >
                  {user.profile_picture_url ? (
                    <img
                      src={user.profile_picture_url}
                      alt="Profile"
                      className="h-8 w-8 rounded-full object-cover"
                    />
                  ) : (
                    <div className="h-8 w-8 bg-indigo-100 dark:bg-indigo-800 rounded-full flex items-center justify-center">
                      <span className="text-indigo-600 dark:text-indigo-300 font-semibold text-sm">
                        {user.email.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                  <span className="text-sm text-gray-700 dark:text-gray-300">{user.email}</span>
                </button>
              )}

              {/* Logout button */}
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-3 sm:px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 shadow-md transition-all"
              >
                <svg className="mr-0 sm:mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Stats Cards */}
          <StatsCards />

          {/* Page Header with Filters */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
            <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">My Tasks</h2>
                <p className="text-gray-500 dark:text-gray-400">Keep track of everything you need to do</p>
              </div>

              {/* Filters */}
              <div className="flex flex-col sm:flex-row gap-3">
                <input
                  type="text"
                  placeholder="Search tasks..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <select
                  value={priorityFilter}
                  onChange={(e) => setPriorityFilter(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">All Priorities</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                </select>
                <button
                  onClick={() => setIsCreating(true)}
                  className="inline-flex items-center justify-center px-6 py-2 border border-transparent text-base font-medium rounded-lg text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg transition-all transform hover:scale-105 whitespace-nowrap"
                >
                  <svg className="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Add Task
                </button>
              </div>
            </div>
          </div>

          {/* Task List */}
          <TaskList
            ref={taskListRef}
            searchQuery={searchQuery}
            priorityFilter={priorityFilter}
            statusFilter={statusFilter}
          />
        </div>
      </main>

      {/* Modals */}
      {isCreating && (
        <CreateTaskForm
          onClose={() => setIsCreating(false)}
          onTaskCreated={handleTaskCreated}
        />
      )}

      {isManagingCategories && (
        <CategoryManager
          onClose={() => setIsManagingCategories(false)}
          onCategoriesChanged={handleCategoriesChanged}
        />
      )}

      {showProfile && (
        <UserProfile onClose={() => setShowProfile(false)} />
      )}
    </div>
  );
}
