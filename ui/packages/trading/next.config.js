/** @type {import('next').NextConfig} */
const path = require('path');

// Get the base path from environment variable or default to '/trading'
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '/trading';

const nextConfig = {
  // Disable strict mode to avoid double rendering in development
  reactStrictMode: false,
  // Set the base path for the app
  basePath,
  // Rewrite API requests to the API gateway
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://api:8000/api/:path*',
      },
    ];
  },
  // Configure webpack
  webpack: (config, { isServer }) => {
    // Force React and React DOM to be loaded from a single location
    config.resolve.alias = {
      ...config.resolve.alias,
      'react': path.resolve(__dirname, '../../node_modules/react'),
      'react-dom': path.resolve(__dirname, '../../node_modules/react-dom'),
    };

    // Prevent multiple instances of React
    config.resolve.modules = [
      path.resolve(__dirname, '../../node_modules'),
      'node_modules',
    ];

    // Remove externals configuration that was causing module not found errors
    // if (!isServer) {
    //   config.externals = {
    //     react: 'React',
    //     'react-dom': 'ReactDOM',
    //   };
    // }

    return config;
  },
};

module.exports = nextConfig;
