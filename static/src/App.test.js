import React from 'react'
import { render, screen } from '@testing-library/react'
import App from './App'

test('renders web page title', () => {
  render(<App />)
  const linkElement = screen.getByText(/Machine Learning web app 💡/i)
  expect(linkElement).toBeInTheDocument()
})
