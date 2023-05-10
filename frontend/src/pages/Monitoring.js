import React, { useEffect, useState } from "react";
import axios from "axios";
import { DateTimePicker } from '@mui/lab';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import LocalizationProvider from '@mui/lab/DatePicker';
import Button from '@mui/material/Button';
import Plot from 'react-plotly.js';


const SensorDataForm = () => {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [sensorData, setSensorData] = useState({});
  const [air_tempp, setAir_tempp] = useState({});
  const [pressurep, setPressurep] = useState({});
  const [air_hump, setAir_hump] = useState({});
  const [soil_hump, setSoil_hump] = useState({});
  const [soil_tempp, setSoil_tempp] = useState({});
  const [lightp, setLightp] = useState({});

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8999/api/getall');
      setSensorData(response.data);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8999/api/getall');
        setSensorData(response.data);
      } catch (error) {
        console.error(error);
      }
    };
  
    fetchData();  }, []);

  useEffect(()=>{
    let air_temp = [];
    let pressure = [];
    let air_hum = [];
    let soil_hum = [];
    let soil_temp = [];
    let light = [];
    if (Object.keys(sensorData)==0)
      return;

    sensorData.map((sensordt) => {
        air_temp['x'].push(sensordt.air_temp)
        air_temp['y'].push(sensordt.timestamp)
        pressure['y'].push(sensordt.timestamp)
        pressure['x'].push(sensordt.pressure)
        air_hum['x'].push(sensordt.air_hum)
        air_hum['y'].push(sensordt.timestamp)
        soil_hum['x'].push(sensordt.soil_hum)
        soil_hum['y'].push(sensordt.timestamp)
        soil_temp['x'].push(sensordt.soil_temp)
        soil_temp['y'].push(sensordt.timestamp)
        light['x'].push(sensordt.light)
        light['y'].push(sensordt.timestamp)
    });
    setAir_tempp({
        x: air_temp['x'],
        y: air_temp['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: getRandomColor()},
      });

      setPressurep({
        x: pressure['x'],
        y: pressure['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: getRandomColor()},
      });

      setAir_hump({
        x: air_hum['x'],
        y: air_hum['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: getRandomColor()},
      });

      setSoil_hump({
        x: soil_hum['x'],
        y: soil_hum['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: getRandomColor()},
      });

      setSoil_tempp({
        x: soil_temp['x'],
        y: soil_temp['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: getRandomColor()},
      });

      setLightp({
        x: light['x'],
        y: light['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: getRandomColor()},
      });
  }, [sensorData])

  return (
    <div>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <DateTimePicker
          label="Start"
          value={start}
          onChange={(newValue) => {
            setStart(newValue);
          }}
        />
        <DateTimePicker
          label="End"
          value={end}
          onChange={(newValue) => {
            setEnd(newValue);
          }}
        />
      </LocalizationProvider>
      {/* <Plot
        data={[
          
          
        ]}
        layout={ {width: 320, height: 240, title: 'A Fancy Plot'} }
      />

      {Plotly.newPlot('myDiv', data, {title: 'Sensor Data', plot_bgcolor: "black", paper_bgcolor: "black", font: {color: "white"}})}
      <Plot
        data={[
          air_tempp,
          // pressurep,
          // air_hump,
          // soil_hump,
          // soil_tempp,
          // lightp
        ]}
        layout={{title: 'Sensor Data', plot_bgcolor: "black", paper_bgcolor: "black", font: {color: "white"}}}/> */}
    </div>
  );
};
const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
export default SensorDataForm;
