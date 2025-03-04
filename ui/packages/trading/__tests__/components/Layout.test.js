import React from 'react';
import { render, screen } from '@testing-library/react';
import Layout from '../../components/Layout';

// Mock the NavBar component
jest.mock('../../components/NavBar', () => {
  return function MockNavBar() {
    return <nav data-testid="mock-navbar">Mock NavBar</nav>;
  };
});

// Mock MUI components
jest.mock('@mui/material', () => ({
  Container: ({ children, maxWidth }) => (
    <div data-testid="mock-container" data-maxwidth={maxWidth}>
      {children}
    </div>
  ),
  CssBaseline: () => <div data-testid="mock-cssbaseline" />,
}));

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

describe('Layout Component', () => {
  it('renders without crashing', () => {
    render(
      <Layout>
        <div data-testid="test-children">Test Children</div>
      </Layout>
    );
    
    // Check if NavBar is rendered
    expect(screen.getByTestId('mock-navbar')).toBeInTheDocument();
    
    // Check if Container is rendered with correct props
    const container = screen.getByTestId('mock-container');
    expect(container).toBeInTheDocument();
    expect(container).toHaveAttribute('data-maxwidth', 'xl');
    
    // Check if children are rendered
    expect(screen.getByTestId('test-children')).toBeInTheDocument();
    expect(screen.getByText('Test Children')).toBeInTheDocument();
    
    // Check if CssBaseline is rendered
    expect(screen.getByTestId('mock-cssbaseline')).toBeInTheDocument();
  });
});
