FROM node:18-alpine

WORKDIR /app

# Copy package.json files
COPY ui/packages/trading/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY ui/packages/trading/ ./

# Build the application
RUN npm run build

# Expose the port
EXPOSE 3005

# Set environment variables
ENV PORT=3005
ENV NEXT_PUBLIC_BASE_PATH=/trading
ENV NODE_ENV=production

# Start the server
CMD ["npm", "start"]
