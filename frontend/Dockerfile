FROM cgr.dev/chainguard/node:latest-dev

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=development

# Expose port
EXPOSE 3000

# Switch to non-root user
USER nonroot

# Start development server
CMD ["npm", "start"]
