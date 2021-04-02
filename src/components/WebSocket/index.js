import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import axios from 'axios';
import socketIOClient from 'socket.io-client';

import CheckBox from '../CheckBox'
import RadioButton from '../RadioButton'


const WebSocket = (props) => {
    const ENDPOINT = props.endpoint
    const optionDescription = props.options

    const [isLoading, setIsLoading] = useState(false);
    const [userId, setUserId] = useState('');
    const [status, setStatus] = useState('');
    const [progress, setProgress] = useState(0);
    const [option, setOption] = useState([]);
    const [time, setTime] = useState('');

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

    return (
        <div>
            {props.type === 'checkbox'
                ? <CheckBox
                    optionDescription={optionDescription}
                    isLoading={isLoading}
                    option={option}
                    setOption={setOption}/>
                : <RadioButton
                    optionDescription={optionDescription}
                    isLoading={isLoading}
                    option={option}
                    setOption={setOption}/>
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

export default WebSocket;