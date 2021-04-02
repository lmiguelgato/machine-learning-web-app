import React from 'react';
import MLCamera from '../../components/MLCamera/index';
import Websocket from '../../components/WebSocket/index';
import AccordionInfo from '../../components/AccordionInfo/index';

const WebCam = (props) => {
    return (
        <>
            <MLCamera
                screenshotFormat="image/jpeg"
                height="200px"
                endpoint={props.endpoint + 'capture'}/>
            <header className="App-header">
            <Websocket endpoint={props.endpoint} options={{0: '🕙', 1: '📈', 2: '💾'}} type="checkbox"/>
            </header>
            <AccordionInfo />
        </>
    );
}

export default WebCam;