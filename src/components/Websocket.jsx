import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup'
import ToggleButton from 'react-bootstrap/ToggleButton'
import axios from 'axios';
import socketIOClient from 'socket.io-client';

const ENDPOINT = 'http://127.0.0.1:5000/';

function Websocket() {
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState('');
  const [status, setStatus] = useState('');
  const [progress, setProgress] = useState(0);
  const [option, setOption] = useState([]);

  const startJob = async () => {
    setIsLoading(true);
    
    const api_response = await axios.post(
      ENDPOINT + 'job',
      {user_id: userId}
    );
    
    setStatus(api_response.data.status);
  }

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    
    socket.on('connected', data => setUserId(data['user_id']));

    socket.on('status', data => {
      if (data.current === data.total) {
        setIsLoading(false);
        setProgress(0);
        setStatus('')
      } else {
        setProgress(Math.floor(100*data.current/data.total));
        setStatus(data.status);
      }
    });
  }, [])

  const handleChange = (val) => setOption(val);

  return (
    <div>
      <Button
      variant="success"
      size="lg"
      disabled={isLoading}
      onClick={!isLoading ? startJob : null}>
      { isLoading ? 'Training model (' + progress + ' %)' : 'Click to train' }
      </Button>
      <br />
      <ToggleButtonGroup type="checkbox" value={option} onChange={handleChange}>
      <ToggleButton variant="outline-success" size="sm" value={1} disabled={isLoading}>Option 1</ToggleButton>
      <ToggleButton variant="outline-success" size="sm" value={2} disabled={isLoading}>Option 2</ToggleButton>
      <ToggleButton variant="outline-success" size="sm" value={3} disabled={isLoading}>Option 3</ToggleButton>      
      </ToggleButtonGroup>
      { option.length > 0
          ? <div>Train with options: {option?.reduce((a, b) => {return a + ' ' + b}, '')}</div>
          : null
      }
      <h4 className="Message">{ status }</h4>
    </div>
  )
}

export default Websocket;