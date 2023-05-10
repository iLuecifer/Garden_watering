import React, { useState, useEffect } from "react";
import {
  IconButton,
  Box,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { DataGrid } from '@mui/x-data-grid';

const SensorDataTable = () => {
  const [data, setData] = useState([]);
  const token = localStorage.getItem("token");
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await fetch("http://127.0.0.1:8999/api/getall/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
    const result = await response.json();
    setData(result);
  };

  const handleRefresh = () => {
    fetchData();
  };

  const columns = [
    { field: "id", headerName: "ID", minWidth: 70 },
    { field: "air_temp", headerName: "Air Temp", minWidth: 120 },
    { field: "pressure", headerName: "Pressure", minWidth: 120 },
    { field: "air_hum", headerName: "Air Humidity", minWidth: 120 },
    { field: "soil_hum", headerName: "Soil Humidity", minWidth: 120 },
    { field: "soil_temp", headerName: "Soil Temp", minWidth: 120 },
    { field: "light", headerName: "Light", minWidth: 120 },
    { field: "timestamp", headerName: "Timestamp", minWidth: 170 },
    { field: "status", headerName: "Status", minWidth: 100, valueGetter: (params) => params.row.status ? "True" : "False" },
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="flex-end" marginBottom={1}>
        <IconButton onClick={handleRefresh}>
          <RefreshIcon />
        </IconButton>
      </Box>
      <div style={{ height: 450, width: '100%' }}>
        <DataGrid
          rows={data}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10]}
          disableSelectionOnClick
        />
      </div>
    </Box>
  );
};

export default SensorDataTable;
