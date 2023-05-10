import React, { useState, useContext } from "react";
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';
import AccountCircle from '@mui/icons-material/AccountCircle';
import axios from "axios";
import { Button, Grid } from '@mui/material';

// Create a context to store the authentication state
const AuthContext = React.createContext({
  isAuthenticated: false,
  login: () => {},
});


function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Make an API call to authenticate the user
      console.log(password,email)
      const response = await axios.post("http://127.0.0.1:8999/api/login/", { 
        username: email,
        password:password 
        });
      login(response.data.token);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container justifyContent="center" spacing={2}>
        <Grid item>
          <UserField setEmail={setEmail} />
        </Grid>
        <Grid item>
          <Password setPassword={setPassword} />
        </Grid>
        <Grid item>
          <SubmitButton />
        </Grid>
      </Grid>
    </form>
  );
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = (token) => {
    // Set the authentication state to true and save the token to local storage
    setIsAuthenticated(true);
    localStorage.setItem("token", token);
  };

  const logout = () => {
    // Set the authentication state to false and remove the token from local storage
    setIsAuthenticated(false);
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {isAuthenticated ? <p>You are logged in.</p> : <LoginForm />}
    </AuthContext.Provider >
    );
}

const Password = (props) => {
    const [showPassword, setShowPassword] = React.useState(false);
  
    const handleClickShowPassword = () => setShowPassword((show) => !show);
  
    const handleChange = (event) => {
      props.setPassword(event.target.value);
    };
  
    return (
      <FormControl sx={{ m: 1, width: '25ch' }} variant="outlined">
        <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
        <OutlinedInput
          id="outlined-adornment-password"
          type={showPassword ? 'text' : 'password'}
          onChange={handleChange}
          endAdornment={
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle password visibility"
                onClick={handleClickShowPassword}
                edge="end"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          }
          label="Password"
        />
      </FormControl>
    );
  };
  

  const UserField = (props) => {
    const handleChange = (event) => {
      props.setEmail(event.target.value);
    };
  
    return (
      <TextField
        id="input-with-icon-textfield"
        label="Email"
        onChange={handleChange}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <AccountCircle />
            </InputAdornment>
          ),
        }}
        variant="standard"
      />
    );
  };

  const SubmitButton = ({ onSubmit, disabled }) => {
    return (
      <Button
        variant="contained"
        color="primary"
        type="submit"
        onClick={onSubmit}
        disabled={disabled}
      >
        Einloggen
      </Button>
    );
  };
export default App;
