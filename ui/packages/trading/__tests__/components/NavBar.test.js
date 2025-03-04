import React from 'react';
import { render, screen } from '@testing-library/react';
import NavBar from '../../components/NavBar';

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

describe('NavBar Component', () => {
  it('renders without crashing', () => {
    render(<NavBar />);
    expect(screen.getByRole('navigation')).toBeInTheDocument();
  });

  it('contains the Trading Dashboard link', () => {
    render(<NavBar />);
    expect(screen.getByText(/Trading Dashboard/i)).toBeInTheDocument();
  });

  it('contains the Backtesting link', () => {
    render(<NavBar />);
    expect(screen.getByText(/Backtesting/i)).toBeInTheDocument();
  });

  it('contains the Model Development link', () => {
    render(<NavBar />);
    expect(screen.getByText(/Model Development/i)).toBeInTheDocument();
  });

  it('contains the Portfolio Monitor link', () => {
    render(<NavBar />);
    expect(screen.getByText(/Portfolio Monitor/i)).toBeInTheDocument();
  });

  it('contains the Strategy Development link', () => {
    render(<NavBar />);
    expect(screen.getByText(/Strategy Development/i)).toBeInTheDocument();
  });

  it('has the correct styling', () => {
    render(<NavBar />);
    const navElement = screen.getByRole('navigation');
    expect(navElement).toHaveStyle('backgroundColor: #1976d2');
  });
});
