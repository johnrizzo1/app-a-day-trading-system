FROM node:18-alpine

WORKDIR /app

# Install Next.js globally
RUN npm install -g next

# Copy package.json files
COPY ui/packages/trading/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY ui/packages/trading/ ./

# Expose the port
EXPOSE 3005

# Set environment variables
ENV PORT=3005
ENV NEXT_PUBLIC_BASE_PATH=/trading

# Start the development server
CMD ["next", "dev", "-p", "3005"]
