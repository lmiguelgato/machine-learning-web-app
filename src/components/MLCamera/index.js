import React from 'react';
import Camera from './camera'

const MLCamera = (props) => {
    return (
            <Camera
                screenshotFormat={props.screenshotFormat}
                height={props.height}
                endpoint={props.endpoint}/>
    );
}

export default MLCamera;