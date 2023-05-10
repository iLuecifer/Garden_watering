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

const MeasureForm = () => {
  const [data, setData] = useState({});
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const token = localStorage.getItem("token");

  const handleClick = () => {
    fetchData();
  }

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8999/api/measure/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      const result = await response.json();
      setData(result.results);
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
      {Object.keys(data).length > 0 ?
        <>
          <TextField fullWidth margin="normal" label="Air Temperature" value={data.air_temp.value + " " + data.air_temp.unit} />
          <TextField fullWidth margin="normal" label="Pressure" value={data.pressure.value+ " " + data.pressure.unit} />
          <TextField fullWidth margin="normal" label="Air Humidity" value={data.air_hum.value+ " " + data.air_hum.unit} />
          <TextField fullWidth margin="normal" label="Soil Humidity" value={data.soil_hum.value+ " " + data.soil_hum.unit} />
          <TextField fullWidth margin="normal" label="Soil Temperature" value={data.soil_temp.value+ " " + data.soil_temp.unit} />
          <TextField fullWidth margin="normal" label="Light" value={data.light.value+ " " + data.light.unit} />
          <FormControlLabel
            control={<Checkbox checked={data.status} />}
            label="Status"
            disabled
          />

        </>
        :
        <>
        <TextField fullWidth margin="normal" label="Air Temperature" value={""} />
        <TextField fullWidth margin="normal" label="Pressure" value={""} />
        <TextField fullWidth margin="normal" label="Air Humidity" value={""} />
        <TextField fullWidth margin="normal" label="Soil Humidity" value={""} />
        <TextField fullWidth margin="normal" label="Soil Temperature" value={""} />
        <TextField fullWidth margin="normal" label="Light" value={""} />
        <FormControlLabel
          control={<Checkbox checked={data.status} />}
          label="Status"
          disabled
        />
      </>
        }
        <>
        <br />
        <Box display="flex" justifyContent="center">
            <Button variant="outlined" startIcon={<RefreshIcon />} onClick={handleClick}>
                Live messen
            </Button>
        </Box>
        <br />
        </>
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
          {error && error.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MeasureForm;
