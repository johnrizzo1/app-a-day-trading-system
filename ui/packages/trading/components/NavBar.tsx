import React from 'react';

// Extremely simple NavBar component without any MUI components
const NavBar = () => {
  return (
    <nav style={{ backgroundColor: '#1976d2', padding: '10px', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ color: 'white', fontWeight: 'bold', fontSize: '20px' }}>WINDSURF</div>
        <div>
          <a href="/trading" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>Trading Dashboard</a>
          <a href="/backtesting" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>Backtesting</a>
          <a href="/model-development" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>Model Development</a>
          <a href="/portfolio-monitor" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>Portfolio Monitor</a>
          <a href="/strategy-development" style={{ color: 'white', margin: '0 10px', textDecoration: 'none' }}>Strategy Development</a>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
