'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth/hooks';

export default function HomePage() {
  console.log('Root page loaded');
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    console.log('Root page mounted');
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isLoading) {
      if (isAuthenticated) {
        router.push('/dashboard');
      } else {
        router.push('/login');
      }
    }
  }, [isLoading, isAuthenticated, router, mounted]);

  // Don't render anything until mounted to avoid hydration mismatch
  if (!mounted) {
    return null;
  }

  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-50">
      <div className="text-center">
        <h2 className="text-xl font-semibold text-gray-700">Loading...</h2>
        <p className="mt-2 text-gray-500">Please wait while we check your session.</p>
      </div>
    </div>
  );
}
