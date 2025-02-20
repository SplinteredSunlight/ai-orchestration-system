import React from 'react';
import {
  CodeBracketIcon,
  PaintBrushIcon,
  MegaphoneIcon,
  BoltIcon,
  ClockIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';

interface Agent {
  id: string;
  name: string;
  type: 'code' | 'design' | 'marketing';
  status: 'idle' | 'busy' | 'error';
  tasksCompleted: number;
  uptime: string;
  lastActive: string;
}

const mockAgents: Agent[] = [
  {
    id: '1',
    name: 'Code Assistant',
    type: 'code',
    status: 'idle',
    tasksCompleted: 24,
    uptime: '99.9%',
    lastActive: '2024-02-20T11:30:00Z',
  },
  {
    id: '2',
    name: 'Design Generator',
    type: 'design',
    status: 'busy',
    tasksCompleted: 18,
    uptime: '98.5%',
    lastActive: '2024-02-20T12:00:00Z',
  },
  {
    id: '3',
    name: 'Marketing Expert',
    type: 'marketing',
    status: 'idle',
    tasksCompleted: 15,
    uptime: '99.2%',
    lastActive: '2024-02-20T10:45:00Z',
  },
];

const Agents: React.FC = () => {
  const getAgentTypeIcon = (type: Agent['type']) => {
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

  const getStatusIcon = (status: Agent['status']) => {
    switch (status) {
      case 'idle':
        return ClockIcon;
      case 'busy':
        return BoltIcon;
      case 'error':
        return XCircleIcon;
      default:
        return ClockIcon;
    }
  };

  const getStatusColor = (status: Agent['status']) => {
    switch (status) {
      case 'idle':
        return 'text-gray-500';
      case 'busy':
        return 'text-yellow-500';
      case 'error':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold leading-7 text-gray-900 dark:text-white sm:truncate sm:text-3xl sm:tracking-tight">
          AI Agents
        </h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Monitor and manage your specialized AI agents
        </p>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {mockAgents.map((agent) => {
          const TypeIcon = getAgentTypeIcon(agent.type);
          const StatusIcon = getStatusIcon(agent.status);
          return (
            <div
              key={agent.id}
              className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg"
            >
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <TypeIcon
                      className="h-6 w-6 text-gray-400"
                      aria-hidden="true"
                    />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="truncate text-sm font-medium text-gray-500 dark:text-gray-400">
                        {agent.name}
                      </dt>
                      <dd className="flex items-center">
                        <StatusIcon
                          className={`h-4 w-4 ${getStatusColor(
                            agent.status
                          )} mr-1`}
                        />
                        <span
                          className={`text-sm ${getStatusColor(agent.status)}`}
                        >
                          {agent.status}
                        </span>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-700 px-5 py-3">
                <div className="text-sm">
                  <div className="flex justify-between text-gray-500 dark:text-gray-400">
                    <span>Tasks completed</span>
                    <span>{agent.tasksCompleted}</span>
                  </div>
                  <div className="flex justify-between text-gray-500 dark:text-gray-400">
                    <span>Uptime</span>
                    <span>{agent.uptime}</span>
                  </div>
                  <div className="flex justify-between text-gray-500 dark:text-gray-400">
                    <span>Last active</span>
                    <span>
                      {new Date(agent.lastActive).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Agents;
