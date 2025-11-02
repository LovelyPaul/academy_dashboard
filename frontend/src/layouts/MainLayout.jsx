/**
 * Main Layout component with header and sidebar.
 * Following the common-modules.md specification.
 */
import React from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  IconButton,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LogoutIcon from '@mui/icons-material/Logout';
import { useAuth } from '../hooks/useAuth';

const DRAWER_WIDTH = 240;

/**
 * Main Layout for dashboard pages.
 * Includes header with user info, sidebar navigation, and main content area.
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Page content
 * @returns {JSX.Element} Main Layout component
 */
export const MainLayout = ({ children }) => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const menuItems = [
    { label: '대시보드', path: '/dashboard' },
    { label: '실적 분석', path: '/dashboard/performance' },
    { label: '논문 분석', path: '/dashboard/papers' },
    { label: '학생 분석', path: '/dashboard/students' },
    { label: '예산 분석', path: '/dashboard/budget' },
    { label: '데이터 업로드', path: '/admin/upload' },
  ];

  const handleLogout = async () => {
    await signOut();
    navigate('/sign-in');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* AppBar (Header) */}
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            대학교 데이터 대시보드
          </Typography>
          <Typography variant="body1" sx={{ mr: 2 }}>
            {user?.primaryEmailAddress?.emailAddress || user?.email}
          </Typography>
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Drawer (Sidebar) */}
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem key={item.path} disablePadding>
                <ListItemButton onClick={() => navigate(item.path)}>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout;
