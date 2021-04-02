import React, { useState } from 'react';
import MLCamera from '../../components/MLCamera/index';
import Websocket from '../../components/WebSocket/index';

const RockPaperScissors = (props) => {
    const [nRocks, setRocks] = useState(0)
    const [nPapers, setPapers] = useState(0)
    const [nScissors, setScissors] = useState(0)

    return (
        <>
            <MLCamera
              screenshotFormat="image/jpeg"
              height="200px"
              endpoint={props.endpoint + 'capture'}/>
            <header className="App-header">
            { nRocks + ' -- ' + nPapers + ' -- ' + nScissors }
            <Websocket endpoint={props.endpoint} options={{0: '✊', 1: '✋', 2: '✌️'}} type="radio"/>
            </header>
        </>
    );
}

export default RockPaperScissors;