import React, { useState, useEffect } from "react";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import Button from '@mui/material/Button';
import CloseIcon from "@mui/icons-material/Close";
import RefreshIcon from "@mui/icons-material/Refresh";
import IconButton from "@mui/material/IconButton";
import axios from "axios";

const MeasureForm = () => {
  const [data, setData] = useState({
    air_temp_min: "",
    air_temp_max: "",  
    air_hum_min: "", 
    air_hum_max: "", 
    soil_temp_min: "", 
    soil_temp_max: "",
    soil_hum_min: "", 
    soil_hum_max: "", 
    light_min: "", 
    light_max: "", 
    pressure_min: "",
    pressure_max: ""
  });
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchData();
  }, []);

  const handleClick = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8999/api/critical_values/", data, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
    } catch (error) {
      setError(error);
      setOpen(true);
    }
  };

  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8999/api/critical_values/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      console.log(response)
      setData(response.data);
    } catch (error) {
      setError(error);
      setOpen(true);
    }
  };

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpen(false);
  };

  return (
    <Box component="form">
      <TextField fullWidth margin="normal" label="Air Temperature Min" value={data.air_temp_min || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal <= data.air_temp_max || !data.air_temp_max) {
            setData({...data, air_temp_min: newVal});
          } else {
            setError('Min value cannot be greater than max value.');
            setOpen(true);
          }
        }} 
        />
      <TextField fullWidth margin="normal" label="Air Temperature Max" value={data.air_temp_max || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal >= data.air_temp_min || !data.air_temp_min) {
            setData({...data, air_temp_max: newVal});
          } else {
            setError('Max value cannot be less than min value.');
            setOpen(true);
          }
        }} 
        />
      <TextField fullWidth margin="normal" label="Air Humidity Min" value={data.air_hum_min || ""} 
                onChange={(e) => {
                  const newVal = parseFloat(e.target.value);
                  if (newVal <= data.air_hum_max || !data.air_hum_max) {
                    setData({...data, air_hum_min: newVal});
                  } else {
                    setError('Min value cannot be greater than max value.');
                    setOpen(true);
                  }
                }}  
        />
      <TextField fullWidth margin="normal" label="Air Humidity Max" value={data.air_hum_max || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal >= data.air_hum_min || !data.air_hum_min) {
            setData({...data, air_hum_max: newVal});
          } else {
            setError('Max value cannot be less than min value.');
            setOpen(true);
          }
        }} 
        />
      <TextField fullWidth margin="normal" label="Soil Temperature Min" value={data.soil_temp_min || ""} 
                onChange={(e) => {
                  const newVal = parseFloat(e.target.value);
                  if (newVal <= data.soil_temp_max || !data.soil_temp_max) {
                    setData({...data, soil_temp_min: newVal});
                  } else {
                    setError('Min value cannot be greater than max value.');
                    setOpen(true);
                  }
                }} 
        />
      <TextField fullWidth margin="normal" label="Soil Temperature Max" value={data.soil_temp_max || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal >= data.soil_temp_min || !data.soil_temp_min) {
            setData({...data, soil_temp_max: newVal});
          } else {
            setError('Max value cannot be less than min value.');
            setOpen(true);
          }
        }} 
/>
      <TextField fullWidth margin="normal" label="Soil Humidity Min" value={data.soil_hum_min || ""} 
                onChange={(e) => {
                  const newVal = parseFloat(e.target.value);
                  if (newVal <= data.soil_hum_max || !data.soil_hum_max) {
                    setData({...data, soil_hum_min: newVal});
                  } else {
                    setError('Min value cannot be greater than max value.');
                    setOpen(true);
                  }
                }} 
        />
      <TextField fullWidth margin="normal" label="Soil Humidity Max" value={data.soil_hum_max || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal >= data.soil_hum_min || !data.soil_hum_min) {
            setData({...data, soil_hum_max: newVal});
          } else {
            setError('Max value cannot be less than min value.');
            setOpen(true);
          }
        }} 
        />
      <TextField fullWidth margin="normal" label="Light Min" value={data.light_min || ""} 
                onChange={(e) => {
                  const newVal = parseFloat(e.target.value);
                  if (newVal <= data.light_max || !data.light_max) {
                    setData({...data, light_min: newVal});
                  } else {
                    setError('Min value cannot be greater than max value.');
                    setOpen(true);
                  }
                }} 
        />
      <TextField fullWidth margin="normal" label="Light Max" value={data.light_max || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal >= data.light_min || !data.light_min) {
            setData({...data, light_max: newVal});
          } else {
            setError('Max value cannot be less than min value.');
            setOpen(true);
          }
        }} 
        />
      <TextField fullWidth margin="normal" label="Pressure Min" value={data.pressure_min || ""} 
                onChange={(e) => {
                  const newVal = parseFloat(e.target.value);
                  if (newVal <= data.pressure_max || !data.pressure_max) {
                    setData({...data, pressure_min: newVal});
                  } else {
                    setError('Min value cannot be greater than max value.');
                    setOpen(true);
                  }
                }} 
        />
      <TextField fullWidth margin="normal" label="Pressure Max" value={data.pressure_max || ""} 
        onChange={(e) => {
          const newVal = parseFloat(e.target.value);
          if (newVal >= data.pressure_min || !data.pressure_min) {
            setData({...data, pressure_max: newVal});
          } else {
            setError('Max value cannot be less than min value.');
            setOpen(true);
          }
        }} 
        />
      <br />
      <Box display="flex" justifyContent="center">
        <Button variant="outlined" startIcon={<RefreshIcon />} onClick={handleClick}>
          Live messen
        </Button>
      </Box>
      <br />
      <Snackbar
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        message="Error fetching data"
        action={
          <>
            <IconButton size="small" aria-label="close" color="inherit" onClick={handleClose}>
              <CloseIcon fontSize="small" />
            </IconButton>
          </>
        }
      >
        <Alert onClose={handleClose} severity="error">
          {error && error.msg ? error + " " + error.message : error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MeasureForm;

