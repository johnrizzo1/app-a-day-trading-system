import React from 'react';
import { render, screen } from '@testing-library/react';
import SimplePage from '../../pages/simple';

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

describe('Simple Page', () => {
  it('renders without crashing', () => {
    render(<SimplePage />);
    expect(screen.getByText('Simple Trading Dashboard')).toBeInTheDocument();
  });

  it('displays the description text', () => {
    render(<SimplePage />);
    expect(
      screen.getByText('This is a simplified version of the trading dashboard without any hooks or complex components.')
    ).toBeInTheDocument();
  });

  it('has the correct heading level', () => {
    render(<SimplePage />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Simple Trading Dashboard');
  });
});
