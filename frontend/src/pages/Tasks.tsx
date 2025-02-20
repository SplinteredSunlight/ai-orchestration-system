import React, { useState } from 'react';
import {
  PlusIcon,
  CodeBracketIcon,
  PaintBrushIcon,
  MegaphoneIcon,
} from '@heroicons/react/24/outline';

interface Task {
  id: string;
  type: 'code' | 'design' | 'marketing';
  title: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  createdAt: string;
}

const mockTasks: Task[] = [
  {
    id: '1',
    type: 'code',
    title: 'Implement user authentication',
    status: 'in_progress',
    progress: 60,
    createdAt: '2024-02-20T10:00:00Z',
  },
  {
    id: '2',
    type: 'design',
    title: 'Create landing page mockup',
    status: 'completed',
    progress: 100,
    createdAt: '2024-02-20T09:30:00Z',
  },
];

const Tasks: React.FC = () => {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const getTaskTypeIcon = (type: Task['type']) => {
    switch (type) {
      case 'code':
        return CodeBracketIcon;
      case 'design':
        return PaintBrushIcon;
      case 'marketing':
        return MegaphoneIcon;
      default:
        return CodeBracketIcon;
    }
  };

  const getStatusColor = (status: Task['status']) => {
    switch (status) {
      case 'pending':
        return 'bg-gray-100 text-gray-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold leading-7 text-gray-900 dark:text-white sm:truncate sm:text-3xl sm:tracking-tight">
            Tasks
          </h2>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Manage and monitor your AI tasks
          </p>
        </div>
        <button
          type="button"
          onClick={() => setIsCreateModalOpen(true)}
          className="btn-primary"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          New Task
        </button>
      </div>

      {/* Task List */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flow-root">
            <ul role="list" className="-my-5 divide-y divide-gray-200 dark:divide-gray-700">
              {mockTasks.map((task) => {
                const Icon = getTaskTypeIcon(task.type);
                return (
                  <li key={task.id} className="py-5">
                    <div className="flex items-center space-x-4">
                      <div className="flex-shrink-0">
                        <Icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium text-gray-900 dark:text-white">
                          {task.title}
                        </p>
                        <div className="flex items-center space-x-2">
                          <span
                            className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getStatusColor(
                              task.status
                            )}`}
                          >
                            {task.status.replace('_', ' ')}
                          </span>
                          <span className="text-sm text-gray-500 dark:text-gray-400">
                            {new Date(task.createdAt).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                      <div className="flex-shrink-0">
                        <div className="relative pt-1 w-24">
                          <div className="overflow-hidden h-2 text-xs flex rounded bg-gray-200 dark:bg-gray-700">
                            <div
                              style={{ width: `${task.progress}%` }}
                              className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-primary-500"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tasks;
