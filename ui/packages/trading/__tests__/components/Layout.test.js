import React from 'react';
import { render, screen } from '@testing-library/react';
import Layout from '../../components/Layout';

// Mock the NavBar component
jest.mock('../../components/NavBar', () => {
  return function MockNavBar() {
    return <nav data-testid="mock-navbar">Mock NavBar</nav>;
  };
});

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
    
    // Check if the main content container is rendered
    const contentContainer = screen.getByText('Test Children').closest('div');
    expect(contentContainer).toBeInTheDocument();
    
    // Check if children are rendered
    expect(screen.getByTestId('test-children')).toBeInTheDocument();
    expect(screen.getByText('Test Children')).toBeInTheDocument();
  });
});
