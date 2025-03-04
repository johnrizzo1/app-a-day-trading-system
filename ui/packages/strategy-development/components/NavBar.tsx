import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box,
  Container,
  useTheme
} from '@mui/material';
import Link from 'next/link';
import { useRouter } from 'next/router';

// Define the navigation items
const navItems = [
  { name: 'Trading', path: 'http://localhost:3005' },
  { name: 'Backtesting', path: 'http://localhost:3001' },
  { name: 'Model Development', path: 'http://localhost:3002' },
  { name: 'Portfolio Monitor', path: 'http://localhost:3003' },
  { name: 'Strategy Development', path: 'http://localhost:3004' }
];

const NavBar: React.FC = () => {
  const theme = useTheme();
  const router = useRouter();

  // Helper function to determine if a nav item is active
  const isActive = (path: string) => {
    // Extract the port from the current URL
    const currentPort = typeof window !== 'undefined' ? window.location.port : '';
    const itemPort = path.split(':')[2]?.split('/')[0];
    return currentPort === itemPort;
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
