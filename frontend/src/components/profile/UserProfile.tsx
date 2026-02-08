'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/lib/auth/hooks';
import { usersApi } from '@/lib/api/users';
import { MdEdit, MdCamera, MdClose } from 'react-icons/md';
import toast from 'react-hot-toast';

interface UserProfileProps {
  onClose: () => void;
}

export default function UserProfile({ onClose }: UserProfileProps) {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [isUploading, setIsUploading] = useState(false);
  const [avatarUrl, setAvatarUrl] = useState(user?.profile_picture_url || '');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setEmail(user.email || '');
      setAvatarUrl(user.profile_picture_url || '');
    }
  }, [user]);

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Preview locally
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);

      // Upload
      handleAvatarUpload(file);
    }
  };

  const handleAvatarUpload = async (file: File) => {
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      toast.error('Please select an image file');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('Image size must be less than 5MB');
      return;
    }

    setIsUploading(true);
    try {
      const response = await usersApi.uploadAvatar(file);
      setAvatarUrl(response.profile_picture_url);
      toast.success('Profile picture updated!');
      setPreviewUrl(null);
    } catch (error: any) {
      console.error('Avatar upload failed:', error);
      toast.error(error.message || 'Failed to upload avatar');
      setPreviewUrl(null);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSaveProfile = async () => {
    try {
      await usersApi.updateProfile({ name });
      toast.success('Profile updated!');
      setIsEditing(false);
    } catch (error: any) {
      console.error('Profile update failed:', error);
      toast.error(error.message || 'Failed to update profile');
    }
  };

  const displayAvatar = previewUrl || avatarUrl;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
        />

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white dark:bg-gray-800 rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-4 flex justify-between items-center">
            <h3 className="text-xl font-bold text-white">User Profile</h3>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 rounded-lg p-2 transition"
            >
              <MdClose size={24} />
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-6">
            {/* Avatar section */}
            <div className="flex flex-col items-center mb-6">
              <div className="relative group">
                {displayAvatar ? (
                  <img
                    src={displayAvatar}
                    alt="Profile"
                    className="w-32 h-32 rounded-full object-cover border-4 border-indigo-500 shadow-lg"
                  />
                ) : (
                  <div className="w-32 h-32 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center border-4 border-indigo-500 shadow-lg">
                    <span className="text-5xl font-bold text-white">
                      {email.charAt(0).toUpperCase()}
                    </span>
                  </div>
                )}

                {/* Camera overlay */}
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isUploading}
                  className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-0 group-hover:bg-opacity-50 rounded-full transition-all"
                >
                  <MdCamera
                    size={32}
                    className="text-white opacity-0 group-hover:opacity-100 transition-opacity"
                  />
                </button>

                {/* Loading spinner */}
                {isUploading && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-full">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
                  </div>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleAvatarChange}
                className="hidden"
              />

              <p className="mt-3 text-sm text-gray-500 dark:text-gray-400">
                Click to upload profile picture
              </p>
            </div>

            {/* Form fields */}
            <div className="space-y-4">
              {/* Email (read-only) */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white cursor-not-allowed"
                />
              </div>

              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Display Name
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    disabled={!isEditing}
                    placeholder="Enter your name"
                    className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100 disabled:dark:bg-gray-800"
                  />
                  {!isEditing && (
                    <button
                      onClick={() => setIsEditing(true)}
                      className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition"
                    >
                      <MdEdit size={20} />
                    </button>
                  )}
                </div>
              </div>

              {/* Save/Cancel buttons */}
              {isEditing && (
                <div className="flex gap-2">
                  <button
                    onClick={handleSaveProfile}
                    className="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition font-medium"
                  >
                    Save Changes
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setName(user?.name || '');
                    }}
                    className="flex-1 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition font-medium"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>

            {/* Stats section */}
            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
              <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Account Info
              </h4>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-indigo-50 dark:bg-indigo-900/30 rounded-lg p-3">
                  <p className="text-xs text-gray-500 dark:text-gray-400">User ID</p>
                  <p className="text-lg font-semibold text-indigo-600 dark:text-indigo-400">
                    #{user?.id || 'N/A'}
                  </p>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">
                  <p className="text-xs text-gray-500 dark:text-gray-400">Member Since</p>
                  <p className="text-sm font-semibold text-purple-600 dark:text-purple-400">
                    {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
