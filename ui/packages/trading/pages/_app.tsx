import React from 'react';
import { AppProps } from 'next/app';
import '../styles/globals.css';

// Helper function to determine if a nav item is active
const isActive = (path: string): boolean => {
  if (typeof window === 'undefined') return false;
  const currentPath = window.location.pathname;
  return currentPath.startsWith(path);
};

// Define the navigation items with updated paths for the API gateway
const navItems = [
  { name: 'Trading', path: '/trading' },
  { name: 'Backtesting', path: '/backtesting' },
  { name: 'Model Development', path: '/model-development' },
  { name: 'Portfolio Monitor', path: '/portfolio-monitor' },
  { name: 'Strategy Development', path: '/strategy-development' }
];

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div>
      {/* Simple navigation bar */}
      <nav style={{ 
        backgroundColor: '#1976d2', 
        marginBottom: '16px',
        padding: '0 16px'
      }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center',
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '8px 0'
        }}>
          <div style={{ 
            marginRight: '16px', 
            color: 'white', 
            fontWeight: 'bold',
            fontSize: '1.25rem'
          }}>
            WINDSURF
          </div>

          <div style={{ display: 'flex', flexGrow: 1 }}>
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.path}
                style={{
                  margin: '8px 16px 8px 0', 
                  color: 'white', 
                  textDecoration: 'none',
                  padding: '8px 16px',
                  backgroundColor: isActive(item.path) ? '#115293' : 'transparent',
                }}
              >
                {item.name}
              </a>
            ))}
          </div>
        </div>
      </nav>

      <div style={{ 
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 16px 20px'
      }}>
        <Component {...pageProps} />
      </div>
    </div>
  );
}

export default MyApp;
