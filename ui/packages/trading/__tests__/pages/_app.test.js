import React from 'react';
import { render } from '@testing-library/react';
import MyApp from '../../pages/_app';

// Mock the CSS imports
jest.mock('../../styles/globals.css', () => ({}));

// Mock component and props
const MockComponent = () => <div data-testid="mock-component">Mock Component</div>;
const mockPageProps = { test: 'test-prop' };

describe('MyApp Component', () => {
  it('renders the component with pageProps', () => {
    const { getByTestId } = render(
      <MyApp Component={MockComponent} pageProps={mockPageProps} />
    );
    
    expect(getByTestId('mock-component')).toBeInTheDocument();
  });
});
