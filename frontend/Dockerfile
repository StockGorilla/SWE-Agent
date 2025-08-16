# Frontend Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 5173

# Start application in preview mode
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
