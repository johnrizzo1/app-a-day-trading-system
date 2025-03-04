FROM node:18-alpine

WORKDIR /app

# Copy package.json for the trading package
COPY ui/packages/trading/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY ui/packages/trading/ ./

# Expose the port
EXPOSE 3005

# Start the development server
CMD ["npm", "run", "dev", "--", "-p", "3005"]
