FROM node:18-alpine

WORKDIR /app

# Create workspace structure
RUN mkdir -p /app/packages/trading /app/packages/shared

# Copy shared package first
COPY ui/packages/shared/package*.json /app/packages/shared/
COPY ui/packages/shared /app/packages/shared/

# Copy trading package
COPY ui/packages/trading/package*.json /app/packages/trading/

# Set up workspace
COPY ui/package.json /app/

# Install dependencies
WORKDIR /app/packages/trading
RUN npm install

# Copy the rest of the application
COPY ui/packages/trading/ /app/packages/trading/

# Build the application
RUN npm run build

# Expose the port
EXPOSE 3005

# Set environment variables
ENV PORT=3005
ENV NEXT_PUBLIC_BASE_PATH=/trading
ENV NODE_ENV=production
ENV NODE_PATH=/app/packages

# Start the server
CMD ["npm", "start"]
