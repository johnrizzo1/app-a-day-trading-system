import React from 'react';
import { render, screen } from '@testing-library/react';
import Custom404 from '../../pages/404';

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

describe('404 Page', () => {
  it('renders without crashing', () => {
    render(<Custom404 />);
    expect(screen.getByText('404')).toBeInTheDocument();
  });

  it('displays the page not found message', () => {
    render(<Custom404 />);
    expect(screen.getByText('Page Not Found')).toBeInTheDocument();
    expect(screen.getByText('The page you are looking for does not exist.')).toBeInTheDocument();
  });

  it('contains a link to the home page', () => {
    render(<Custom404 />);
    const homeLink = screen.getByText('Return to Home');
    expect(homeLink).toBeInTheDocument();
    // In Next.js Link implementation, it's actually a div inside an anchor
    const linkContainer = homeLink.closest('a');
    expect(linkContainer).toHaveAttribute('href', '/');
  });

  it('has the correct styling', () => {
    render(<Custom404 />);
    const homeLink = screen.getByText('Return to Home');
    expect(homeLink).toHaveStyle({
      backgroundColor: '#1976d2',
      color: 'white',
      padding: '8px 16px',
      borderRadius: '4px',
      textDecoration: 'none',
      fontWeight: 'bold',
    });
  });
});
