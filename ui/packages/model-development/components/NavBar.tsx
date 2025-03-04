import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  Container,
  createTheme
} from '@mui/material';
import Link from 'next/link';

// Define the navigation items
const navItems = [
  { name: 'Trading', path: '/trading' },
  { name: 'Backtesting', path: '/backtesting' },
  { name: 'Model Development', path: '/model-development' },
  { name: 'Portfolio Monitor', path: '/portfolio-monitor' },
  { name: 'Strategy Development', path: '/strategy-development' }
];

// Create a theme instance for use in static methods
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      dark: '#115293',
    },
  },
});

const NavBar: React.FC = () => {
  // Helper function to determine if a nav item is active
  const isActive = (path: string) => {
    if (typeof window === 'undefined') return false;
    const currentPath = window.location.pathname;
    return currentPath.startsWith(path);
  };

  return (
    <AppBar position="static" sx={{ marginBottom: 2 }}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
          >
            WINDSURF
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {navItems.map((item) => (
              <Button
                key={item.name}
                component="a"
                href={item.path}
                sx={{
                  my: 2, 
                  color: 'white', 
                  display: 'block',
                  backgroundColor: isActive(item.path) ? theme.palette.primary.dark : 'transparent',
                  '&:hover': {
                    backgroundColor: theme.palette.primary.dark,
                  }
                }}
              >
                {item.name}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default NavBar;
