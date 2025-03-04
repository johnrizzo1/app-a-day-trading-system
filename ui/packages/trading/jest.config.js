module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/', '<rootDir>/pages/test.tsx'],
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
  moduleNameMapper: {
    '^@/components/(.*)$': '<rootDir>/components/$1',
    '^@/pages/(.*)$': '<rootDir>/pages/$1',
    '^@/hooks/(.*)$': '<rootDir>/hooks/$1',
    '^@/utils/(.*)$': '<rootDir>/utils/$1',
  },
  collectCoverageFrom: [
    'components/**/*.{js,jsx,ts,tsx}',
    'pages/**/*.{js,jsx,ts,tsx}',
    'hooks/**/*.{js,jsx,ts,tsx}',
    'utils/**/*.{js,jsx,ts,tsx}',
    '!pages/_app.js',
    '!pages/_document.js',
    '!pages/test.tsx',
    '!pages/index.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50,
    },
    './components/NavBar.tsx': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    './pages/_app.tsx': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    './pages/minimal.js': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    './pages/standalone.js': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
  },
  transformIgnorePatterns: [
    '/node_modules/(?!(@mui|recharts)/)',
  ],
  testMatch: ['**/__tests__/**/*.test.js'],
};
