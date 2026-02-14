import { render, screen } from '@testing-library/react';
import App from './App';

test('renders AI Content Generator', () => {
  render(<App />);
  const heading = screen.getByText(/AI Content Generator/i);
  expect(heading).toBeInTheDocument();
});
