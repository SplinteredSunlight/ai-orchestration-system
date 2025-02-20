import React, { Fragment } from 'react';
import { NavLink } from 'react-router-dom';
import { Dialog, Transition } from '@headlessui/react';
import {
  XMarkIcon,
  HomeIcon,
  QueueListIcon,
  UserGroupIcon,
  CogIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Tasks', href: '/tasks', icon: QueueListIcon },
  { name: 'Agents', href: '/agents', icon: UserGroupIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const NavItem = ({ item }: { item: typeof navigation[0] }) => {
    return (
      <NavLink
        to={item.href}
        className={({ isActive }) =>
          `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
            isActive
              ? 'bg-primary-700 text-white'
              : 'text-gray-300 hover:bg-primary-700 hover:text-white'
          }`
        }
      >
        <item.icon
          className="mr-3 h-6 w-6 flex-shrink-0"
          aria-hidden="true"
        />
        {item.name}
      </NavLink>
    );
  };

  return (
    <>
      {/* Mobile sidebar */}
      <Transition.Root show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-50 lg:hidden" onClose={onClose}>
          <Transition.Child
            as={Fragment}
            enter="transition-opacity ease-linear duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-linear duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-gray-900/80" />
          </Transition.Child>

          <div className="fixed inset-0 flex">
            <Transition.Child
              as={Fragment}
              enter="transition ease-in-out duration-300 transform"
              enterFrom="-translate-x-full"
              enterTo="translate-x-0"
              leave="transition ease-in-out duration-300 transform"
              leaveFrom="translate-x-0"
              leaveTo="-translate-x-full"
            >
              <Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
                <div className="flex h-full flex-col overflow-y-auto bg-primary-800 px-6 py-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <img
                        className="h-8 w-auto"
                        src="/logo.svg"
                        alt="AI Orchestration"
                      />
                      <span className="ml-2 text-xl font-bold text-white">
                        AI Orchestration
                      </span>
                    </div>
                    <button
                      type="button"
                      className="text-gray-300 hover:text-white"
                      onClick={onClose}
                    >
                      <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                    </button>
                  </div>
                  <nav className="mt-8 flex-1">
                    <ul role="list" className="flex flex-1 flex-col gap-y-7">
                      <li>
                        <ul role="list" className="-mx-2 space-y-1">
                          {navigation.map((item) => (
                            <li key={item.name}>
                              <NavItem item={item} />
                            </li>
                          ))}
                        </ul>
                      </li>
                    </ul>
                  </nav>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition.Root>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64">
        <div className="flex min-h-0 flex-1 flex-col bg-primary-800">
          <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
            <div className="flex flex-shrink-0 items-center px-4">
              <img
                className="h-8 w-auto"
                src="/logo.svg"
                alt="AI Orchestration"
              />
              <span className="ml-2 text-xl font-bold text-white">
                AI Orchestration
              </span>
            </div>
            <nav className="mt-8 flex-1 px-2">
              <ul role="list" className="flex flex-1 flex-col gap-y-7">
                <li>
                  <ul role="list" className="-mx-2 space-y-1">
                    {navigation.map((item) => (
                      <li key={item.name}>
                        <NavItem item={item} />
                      </li>
                    ))}
                  </ul>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
