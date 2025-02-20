import React from 'react';
import { ChartBarIcon, ClockIcon, ServerIcon } from '@heroicons/react/24/outline';

const stats = [
  {
    name: 'Active Tasks',
    value: '12',
    change: '+2',
    changeType: 'increase',
    icon: ClockIcon,
  },
  {
    name: 'Available Agents',
    value: '3',
    change: '0',
    changeType: 'neutral',
    icon: ServerIcon,
  },
  {
    name: 'API Cost',
    value: '$2.50',
    change: '-$0.50',
    changeType: 'decrease',
    icon: ChartBarIcon,
  },
];

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold leading-7 text-gray-900 dark:text-white sm:truncate sm:text-3xl sm:tracking-tight">
          Dashboard
        </h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Overview of your AI orchestration system
        </p>
      </div>

      {/* Stats */}
      <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="relative overflow-hidden rounded-lg bg-white dark:bg-gray-800 px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6"
          >
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500 dark:text-gray-400">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                {stat.value}
              </p>
              <p
                className={`ml-2 flex items-baseline text-sm font-semibold ${
                  stat.changeType === 'increase'
                    ? 'text-green-600'
                    : stat.changeType === 'decrease'
                    ? 'text-red-600'
                    : 'text-gray-500'
                }`}
              >
                {stat.change}
              </p>
            </dd>
          </div>
        ))}
      </dl>

      {/* Recent Tasks */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900 dark:text-white">
            Recent Tasks
          </h3>
        </div>
        <div className="border-t border-gray-200 dark:border-gray-700">
          <div className="px-4 py-5 sm:p-6">
            <p className="text-gray-500 dark:text-gray-400">
              No recent tasks to display
            </p>
          </div>
        </div>
      </div>

      {/* Agent Status */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900 dark:text-white">
            Agent Status
          </h3>
        </div>
        <div className="border-t border-gray-200 dark:border-gray-700">
          <div className="px-4 py-5 sm:p-6">
            <p className="text-gray-500 dark:text-gray-400">
              All agents are currently idle
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
