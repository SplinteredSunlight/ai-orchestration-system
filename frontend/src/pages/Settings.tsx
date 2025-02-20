import React, { useState } from 'react';
import {
  CogIcon,
  BellIcon,
  KeyIcon,
  CurrencyDollarIcon,
  ServerIcon,
} from '@heroicons/react/24/outline';

interface SettingsSection {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<any>;
  fields: {
    id: string;
    label: string;
    type: 'text' | 'number' | 'toggle' | 'select';
    value: any;
    options?: { value: string; label: string }[];
    description?: string;
  }[];
}

const settingsSections: SettingsSection[] = [
  {
    id: 'api',
    name: 'API Configuration',
    description: 'Manage API keys and endpoints for AI services',
    icon: KeyIcon,
    fields: [
      {
        id: 'openai_key',
        label: 'OpenAI API Key',
        type: 'text',
        value: '••••••••••••••••',
        description: 'Your OpenAI API key for model access',
      },
      {
        id: 'model_preference',
        label: 'Default Model',
        type: 'select',
        value: 'gpt-3.5-turbo',
        options: [
          { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
          { value: 'gpt-4', label: 'GPT-4' },
        ],
      },
    ],
  },
  {
    id: 'cost',
    name: 'Cost Management',
    description: 'Configure cost limits and notifications',
    icon: CurrencyDollarIcon,
    fields: [
      {
        id: 'cost_limit',
        label: 'Cost Limit ($)',
        type: 'number',
        value: 5,
        description: 'Maximum API cost before requiring confirmation',
      },
      {
        id: 'cost_notifications',
        label: 'Cost Notifications',
        type: 'toggle',
        value: true,
        description: 'Receive notifications when approaching cost limit',
      },
    ],
  },
  {
    id: 'agents',
    name: 'Agent Configuration',
    description: 'Configure AI agent behavior and resources',
    icon: ServerIcon,
    fields: [
      {
        id: 'parallel_tasks',
        label: 'Maximum Parallel Tasks',
        type: 'number',
        value: 3,
        description: 'Maximum number of tasks to run simultaneously',
      },
      {
        id: 'verification',
        label: 'Result Verification',
        type: 'toggle',
        value: true,
        description: 'Verify agent outputs with high-quality models',
      },
    ],
  },
  {
    id: 'notifications',
    name: 'Notifications',
    description: 'Manage system notifications and alerts',
    icon: BellIcon,
    fields: [
      {
        id: 'email_notifications',
        label: 'Email Notifications',
        type: 'toggle',
        value: true,
        description: 'Receive task completion notifications via email',
      },
      {
        id: 'error_alerts',
        label: 'Error Alerts',
        type: 'toggle',
        value: true,
        description: 'Receive immediate alerts for system errors',
      },
    ],
  },
];

const Settings: React.FC = () => {
  const [settings, setSettings] = useState(settingsSections);

  const handleInputChange = (sectionId: string, fieldId: string, value: any) => {
    setSettings(
      settings.map((section) =>
        section.id === sectionId
          ? {
              ...section,
              fields: section.fields.map((field) =>
                field.id === fieldId ? { ...field, value } : field
              ),
            }
          : section
      )
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold leading-7 text-gray-900 dark:text-white sm:truncate sm:text-3xl sm:tracking-tight">
          Settings
        </h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Configure your AI orchestration system
        </p>
      </div>

      <div className="space-y-6">
        {settings.map((section) => (
          <div
            key={section.id}
            className="bg-white dark:bg-gray-800 shadow rounded-lg"
          >
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <section.icon
                  className="h-6 w-6 text-gray-400"
                  aria-hidden="true"
                />
                <div className="ml-3">
                  <h3 className="text-lg font-medium leading-6 text-gray-900 dark:text-white">
                    {section.name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    {section.description}
                  </p>
                </div>
              </div>

              <div className="mt-6 space-y-6">
                {section.fields.map((field) => (
                  <div key={field.id} className="flex flex-col space-y-2">
                    <label
                      htmlFor={field.id}
                      className="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >
                      {field.label}
                    </label>
                    {field.type === 'toggle' ? (
                      <button
                        type="button"
                        className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                          field.value ? 'bg-primary-600' : 'bg-gray-200'
                        }`}
                        role="switch"
                        aria-checked={field.value}
                        onClick={() =>
                          handleInputChange(section.id, field.id, !field.value)
                        }
                      >
                        <span
                          aria-hidden="true"
                          className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                            field.value ? 'translate-x-5' : 'translate-x-0'
                          }`}
                        />
                      </button>
                    ) : field.type === 'select' ? (
                      <select
                        id={field.id}
                        value={field.value}
                        onChange={(e) =>
                          handleInputChange(section.id, field.id, e.target.value)
                        }
                        className="input"
                      >
                        {field.options?.map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type={field.type}
                        id={field.id}
                        value={field.value}
                        onChange={(e) =>
                          handleInputChange(
                            section.id,
                            field.id,
                            field.type === 'number'
                              ? Number(e.target.value)
                              : e.target.value
                          )
                        }
                        className="input"
                      />
                    )}
                    {field.description && (
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {field.description}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Settings;
