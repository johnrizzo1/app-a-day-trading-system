import React from 'react';
import { render, screen } from '@testing-library/react';
import StandalonePage from '../../pages/standalone';

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

describe('Standalone Page', () => {
  it('renders without crashing', () => {
    render(<StandalonePage />);
    expect(screen.getByText('Standalone Page')).toBeInTheDocument();
  });

  it('displays the description text', () => {
    render(<StandalonePage />);
    expect(screen.getByText('This is a completely standalone page without any dependencies.')).toBeInTheDocument();
  });

  it('has the correct heading level', () => {
    render(<StandalonePage />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Standalone Page');
  });
});
