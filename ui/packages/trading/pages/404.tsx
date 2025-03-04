import React from 'react';

export default function Custom404() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      padding: '24px',
      textAlign: 'center',
    }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '16px' }}>404</h1>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '16px' }}>Page Not Found</h2>
      <p style={{ marginBottom: '24px' }}>The page you are looking for does not exist.</p>
      <a 
        href="/" 
        style={{
          backgroundColor: '#1976d2',
          color: 'white',
          padding: '8px 16px',
          borderRadius: '4px',
          textDecoration: 'none',
          fontWeight: 'bold',
        }}
      >
        Return to Home
      </a>
    </div>
  );
}
