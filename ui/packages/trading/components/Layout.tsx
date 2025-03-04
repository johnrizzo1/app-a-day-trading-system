import React, { ReactNode } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import NavBar from './NavBar';

interface LayoutProps {
  children: ReactNode;
}

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar />
      <Container maxWidth="xl">
        {children}
      </Container>
    </ThemeProvider>
  );
};

export default Layout;
