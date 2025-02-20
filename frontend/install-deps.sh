#!/bin/bash

# Install React and core dependencies
npm install --legacy-peer-deps \
  @types/react \
  @types/react-dom \
  @types/node \
  @types/jest

# Install routing dependencies
npm install --legacy-peer-deps \
  @types/react-router-dom

# Install UI component libraries
npm install --legacy-peer-deps \
  @headlessui/react \
  @heroicons/react

# Install state management and data fetching
npm install --legacy-peer-deps \
  zustand \
  @tanstack/react-query

# Install development dependencies
npm install --legacy-peer-deps -D \
  typescript@4.9.5 \
  @typescript-eslint/eslint-plugin \
  @typescript-eslint/parser \
  eslint-plugin-react \
  eslint-plugin-react-hooks \
  prettier \
  @types/tailwindcss

# Install Tailwind and its dependencies
npm install --legacy-peer-deps -D \
  tailwindcss \
  postcss \
  autoprefixer \
  @tailwindcss/forms
