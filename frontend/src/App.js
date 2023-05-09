import Login from './pages/login.js'
import LiveCam from './pages/live.js'
import Relais from './pages/Relais.js'
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';

function RequireAuth({ children }) {
  let auth = localStorage.getItem("token")
  let location = useLocation();

  if (!auth) {
    return <Navigate to="/login" state={{ from: location }} />;
  }

  return children;
}

function App() {
  return (
    <div className="App">
    <Router>
        <Routes>
        <Route
          path="/live"
          element={
            <RequireAuth>
              <LiveCam />
            </RequireAuth>
          }
        />
             <Route
          path="/pumpe"
          element={
            <RequireAuth>
              <Relais />
            </RequireAuth>
          }
        />
        <Route exact path="/login" element={<Login />} />              
        </ Routes>
      </Router>
    </div>
    
  );
}

export default App;
