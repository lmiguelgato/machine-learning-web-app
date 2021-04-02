import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup'
import ToggleButton from 'react-bootstrap/ToggleButton'
import axios from 'axios';
import socketIOClient from 'socket.io-client';

const ENDPOINT = 'http://127.0.0.1:5000/';

function Websocket(props) {
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState('');
  const [status, setStatus] = useState('');
  const [progress, setProgress] = useState(0);
  const [option, setOption] = useState([]);
  const [time, setTime] = useState('');

  const optionDescription = props.options

  const startJob = async () => {
    setIsLoading(true);
    
    const api_response = await axios.post(
      ENDPOINT + 'job',
      {user_id: userId}
    );
    
    setTime(api_response.data.status);
  }

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    
    socket.on('connected', data => setUserId(data['user_id']));

    socket.on('status', data => {
      if (data.current === data.total) {
        setIsLoading(false);
        setProgress(0);
        setStatus('')
        setTime(start => start + ', finished at ' + data.time);
      } else {
        setProgress(Math.floor(100*data.current/data.total));
        setStatus(data.status);
      }
    });
  }, [])

  const handleChange = (val) => setOption(val);

  return (
    <div>
      <ToggleButtonGroup name="options" value={option} type={props.type} onChange={handleChange}>
        {Object.keys(optionDescription).map((key) => {
          return (
            <ToggleButton
            key={key}
            disabled={isLoading}
            variant="outline-success"
            size="sm"
            value={key+1}>
              {optionDescription[key]}
            </ToggleButton>    
          )
        })}
      </ToggleButtonGroup>
      <br />
      { isLoading
          ? (option.length && props.type === "checkbox") 
            ? option.length === 1 
              ? <div>Training with option: { optionDescription[option[0][0]]}</div>
              : <div>Training with options: { option.map((i) => {return optionDescription[i[0]]}) }</div>
            : null
          : null
      }
      <br />
      <Button
      variant="success"
      size="lg"
      disabled={isLoading}
      onClick={!isLoading ? startJob : null}
      className="Button">
      { isLoading ? '🧠 Training model (' + progress + ' %)' : '🚀 Click to train' }
      </Button>
      <br />
      { time }
      <h4 className="Message">{ status }</h4>
    </div>
  )
}

export default Websocket;