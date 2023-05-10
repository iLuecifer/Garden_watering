import React, { useState } from 'react';
import Login from './pages/login.js'
import LiveCam from './pages/live.js'
import Relais from './pages/Relais.js'
import Measure from './pages/Measure.js'
import Menu from './pages/Menu.js'
import SensorDataTable from './pages/SensorDT.js';
import RelaisLogsTable from './pages/RelaisLogs.js';
import CriticalForm from './pages/CriticalForm.js';
import Monitoring from './pages/Monitoring.js';
import { Box } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';


const theme = createTheme({
  palette: {
    mode: 'dark', 
    primary: {
      main: '#99cc00', 
    },
    secondary: {
      main: '#133a13', 
    },
    text: {
      primary: '#ffffff',
      secondary: '#ffffff',
    },

  },
  components: {
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "#133a13"
          },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#133a13"
          }
        },
        notchedOutline: {
          borderColor: '#133a13',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiInput-input': {
            color: '#ffffff',
            backgroundColor:'#000000'
          },
          '& .MuiInputLabel-root': {
            color: '#99cc00',
            backgroundColor:'#333333',
          },
        },
      },
    },
    MuiDataGrid: {
      styleOverrides: {
        root: {
          backgroundColor: '#282c34', // Change this to your preferred color
          color: '#ffffff',
          '& .MuiDataGrid-cell': {
            color: '#ffffff',
          },
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: '#ffffff',
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        root: {
          color: '#ffffff',
          backgroundColor: '#333333', // Change this to the color you want
        },
        input: {
          color: '#ffffff',
        },
      },
    },
    typography: {
      styleOverrides: {
      // Name of the slot
      root: {
        input: {
          color: '#ffffff',
        },
        backgroundColor: 'black'
      },
    },
    chip: {
      root: {
        backgroundColor: 'black',
        color:'#99cc00',
       }
      }
    },
  }
});


function RequireAuth({ children }) {
  let auth = localStorage.getItem("token")
  let location = useLocation();

  if (!auth) {
    return <Navigate to="/login" state={{ from: location }} />;
  }

  return children;
}

function App() {
  const [selectedComponent, setSelectedComponent] = useState(0);

  const handleMenuChange = (index) => {
    setSelectedComponent(index);
  };

  const renderSelectedComponent = () => {
    switch (selectedComponent) {
      case 0:
        return <SensorDataTable />;
      case 1:
        return <RelaisLogsTable />;
      case 2:
        return <LiveCam />;
      case 3:
        return <Measure />;
      case 4:
        return <Relais />;
      case 5:
        return <CriticalForm />;
      case 6:
        return <Monitoring />;
      default:
        return null;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <Router>
          <Routes>
            <Route exact path="/" element={<RequireAuth>
              <Box display="flex">
                <Menu onChange={handleMenuChange} />
                <Box flexGrow={1} p={2}>
                  <Box paddingLeft={12}>{renderSelectedComponent()}</Box>
                </Box>
              </Box>
            </RequireAuth>}/> 

            <Route exact path="/login" element={<Login />}/>              
          </ Routes>
        </Router>
      </div>
    </ThemeProvider>
  );
}

export default App;
