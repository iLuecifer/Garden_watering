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
    let air_temp = { 'x': [], 'y': [] };
    let pressure = { 'x': [], 'y': [] };
    let air_hum = { 'x': [], 'y': [] };
    let soil_hum = { 'x': [], 'y': [] };
    let soil_temp = { 'x': [], 'y': [] };
    let light = { 'x': [], 'y': [] };

    if (Object.keys(sensorData)==0)
      return;

    sensorData.map((sensordt) => {
        air_temp['y'].push(sensordt.air_temp)
        air_temp['x'].push(sensordt.timestamp)
        pressure['x'].push(sensordt.timestamp)
        pressure['y'].push(sensordt.pressure)
        air_hum['y'].push(sensordt.air_hum)
        air_hum['x'].push(sensordt.timestamp)
        soil_hum['y'].push(sensordt.soil_hum)
        soil_hum['x'].push(sensordt.timestamp)
        soil_temp['y'].push(sensordt.soil_temp)
        soil_temp['x'].push(sensordt.timestamp)
        light['y'].push(sensordt.light)
        light['x'].push(sensordt.timestamp)
    });
    setAir_tempp({
        x: air_temp['x'],
        y: air_temp['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: '#00ccff'},
        name: 'Luft',
      });

      setPressurep({
        x: pressure['x'],
        y: pressure['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: '#ff66ff'},
        name: 'Luft',
      });

      setAir_hump({
        x: air_hum['x'],
        y: air_hum['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: '#00ffcc'},
        name: 'Luft',
      });

      setSoil_hump({
        x: soil_hum['x'],
        y: soil_hum['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: '#996633'},
        name: 'Erde ',
      });

      setSoil_tempp({
        x: soil_temp['x'],
        y: soil_temp['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: '#ff9966'},
        name: 'Erde ',
      });

      setLightp({
        x: light['x'],
        y: light['y'],
        type: 'scatter',
        mode: 'lines+points',
        marker: {color: '#ffff66'},
        name: 'Erde ',
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
       <Plot
        data={[
          air_tempp,
          soil_tempp
        ]}
        layout={ {title: 'Temperatur in C°', plot_bgcolor: "black", paper_bgcolor: "black", font: {color: "white"}} }
      />
        <Plot
        data={[
          air_hump,
          soil_hump
        ]}
        layout={ {title: 'Feutchtigkeit in %', plot_bgcolor: "black", paper_bgcolor: "black", font: {color: "white"}} }
      />
        <Plot
        data={[
          lightp
        ]}
        layout={ {title: 'Licht in Lux', plot_bgcolor: "black", paper_bgcolor: "black", font: {color: "white"}} }
      />
        <Plot
        data={[
          pressurep
        ]}
        layout={ {title: 'Druck in hPa', plot_bgcolor: "black", paper_bgcolor: "black", font: {color: "white"}} }
      />
   
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
