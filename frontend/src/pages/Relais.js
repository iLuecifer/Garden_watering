import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import axios from "axios";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";


export default function BasicButtons() {
    const token = localStorage.getItem("token");
  
    const [open, setOpen] = React.useState(false);
    const [alertSeverity, setAlertSeverity] = React.useState("success");
    const [alertMessage, setAlertMessage] = React.useState("");
    
    const [stat, setStat] = React.useState("aktivieren")

    const handleClose = (event, reason) => {
      if (reason === "clickaway") {
        return;
      }
      setOpen(false);
    };
  
    async function handleEnableClick() {
      try {
        const response = await axios.get("http://127.0.0.1:8999/api/enable_relais/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setAlertMessage("Pumpe aktiviert");
        setAlertSeverity("success");
        setOpen(true);
      } catch (error) {
        setAlertMessage("Fehler beim Aktivieren der Pumpe");
        setAlertSeverity("error");
        setOpen(true);
      }
    }
  
    async function handleDisableClick() {
      try {
        const response = await axios.get("http://127.0.0.1:8999/api/disable_relais/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setAlertMessage("Pumpe deaktiviert");
        setAlertSeverity("success");
        setOpen(true);
      } catch (error) {
        setAlertMessage("Fehler beim Deaktivieren der Pumpe");
        setAlertSeverity("error");
        setOpen(true);
      }
    }
  
    async function handleMotionClick() {
      try {
        const response = await axios.get("http://127.0.0.1:8999/api/run_motion_detection/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        if(response.data.command == "start")
        {
            setAlertMessage("Bewegungssensor aktiviert");
            setStat("deaktivieren")
            setAlertSeverity("success");
        }else{
            setAlertMessage("Bewegungssensor deaktiviert");
            setStat("aktivieren")
            setAlertSeverity("success");
        }
        setOpen(true);
      } catch (error) {
        setAlertMessage("Fehler beim Aktivieren des Bewegungssensors");
        setAlertSeverity("error");
        setOpen(true);
      }
    }
  
    return (
      <div>
        <Stack spacing={2} direction="row">
          <Button variant="text" onClick={handleEnableClick}>
            Pumpe aktivieren
          </Button>
          <Button variant="text" onClick={handleDisableClick}>
            Pumpe deaktivieren
          </Button>
          <Button variant="text" onClick={handleMotionClick}>
            Bewegungssensor {stat}
          </Button>
        </Stack>
        <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
          <Alert onClose={handleClose} severity={alertSeverity} sx={{ width: "100%" }}>
            {alertMessage}
          </Alert>
        </Snackbar>
      </div>
    );
  }
  
