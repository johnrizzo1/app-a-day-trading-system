import React from 'react';
import Link from 'next/link';

export default function Custom404() {
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
            <a href="/trading" style={{ margin: '8px 16px 8px 0', color: 'white', textDecoration: 'none', padding: '8px 16px' }}>Trading</a>
            <a href="/backtesting" style={{ margin: '8px 16px 8px 0', color: 'white', textDecoration: 'none', padding: '8px 16px' }}>Backtesting</a>
            <a href="/model-development" style={{ margin: '8px 16px 8px 0', color: 'white', textDecoration: 'none', padding: '8px 16px' }}>Model Development</a>
            <a href="/portfolio-monitor" style={{ margin: '8px 16px 8px 0', color: 'white', textDecoration: 'none', padding: '8px 16px' }}>Portfolio Monitor</a>
            <a href="/strategy-development" style={{ margin: '8px 16px 8px 0', color: 'white', textDecoration: 'none', padding: '8px 16px' }}>Strategy Development</a>
          </div>
        </div>
      </nav>

      {/* 404 content */}
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 16px',
      }}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '80vh',
          padding: '24px',
          textAlign: 'center',
        }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '16px' }}>404</h1>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '16px' }}>Page Not Found</h2>
          <p style={{ marginBottom: '24px' }}>The page you are looking for does not exist.</p>
          <Link href="/" passHref>
            <div
              style={{
                backgroundColor: '#1976d2',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '4px',
                textDecoration: 'none',
                fontWeight: 'bold',
                cursor: 'pointer',
              }}
            >
              Return to Home
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
