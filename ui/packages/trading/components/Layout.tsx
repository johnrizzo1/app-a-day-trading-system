import React from 'react';
import NavBar from './NavBar';

type LayoutProps = {
  children: React.ReactNode;
};

// Very simplified Layout component to avoid type conflicts
const Layout = ({ children }: LayoutProps) => {
  return (
    <div>
      <NavBar />
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 16px' }}>
        {children}
      </div>
    </div>
  );
};

export default Layout;
