import React from 'react';
import { render, screen } from '@testing-library/react';
import MinimalPage from '../../pages/minimal';

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

describe('Minimal Page', () => {
  it('renders without crashing', () => {
    render(<MinimalPage />);
    expect(screen.getByText('Minimal Page')).toBeInTheDocument();
  });

  it('displays the description text', () => {
    render(<MinimalPage />);
    expect(screen.getByText('This is a minimal page with no dependencies.')).toBeInTheDocument();
  });

  it('has the correct heading level', () => {
    render(<MinimalPage />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Minimal Page');
  });
});
