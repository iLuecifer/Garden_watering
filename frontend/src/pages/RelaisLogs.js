import React, { useState, useEffect } from "react";
import { IconButton, Box } from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { DataGrid } from '@mui/x-data-grid';

const WaterPumpLogsTable = () => {
  const [data, setData] = useState([]);
  const token = localStorage.getItem("token");
  
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await fetch("http://127.0.0.1:8999/api/relais_data/", {
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
    { field: "start", headerName: "Start", minWidth: 170 },
    { field: "end", headerName: "End", minWidth: 170 },
    { field: "user", headerName: "User", minWidth: 120 },
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

export default WaterPumpLogsTable;
