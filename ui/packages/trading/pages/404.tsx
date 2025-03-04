import React from 'react';
import Link from 'next/link';
import Layout from '../components/Layout';

export default function Custom404() {
  return (
    <Layout>
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
    </Layout>
  );
}
