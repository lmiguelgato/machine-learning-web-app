import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from 'react-webcam'
import axios from 'axios';

const Camera = (props) => {
    const [capture, setCapture] = useState(false);

    const webcamRef = React.useRef(null);

    const takePicture = React.useCallback(
    async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        const api_response = await axios.post(
            props.endpoint,
            {data_uri: imageSrc}
        );
        console.log(api_response)
    }, [webcamRef]);

    const toggleOnOff = () => {
        if (capture) {
        setCapture(false)
        } else {
        setCapture(true)
        }
    }

    return (
        <>
            { capture?
                <>
                    <Webcam audio={false}
                    screenshotFormat={props.screenshotFormat}
                    ref={webcamRef}
                    height={props.height}
                    className="WebCam"/>
                    <br />
                    <Button
                        variant="success"
                        size="sm"
                        onClick={takePicture}
                        className="Button">
                        📷 Capture
                    </Button>
                </>
                : null
            }
            <Button
                className="Button"
                variant="success"
                size="sm"
                onClick={toggleOnOff}>
                { capture ? '⛔ Turn off webcam' : '🎥 Turn on webcam' }
            </Button>
        </>
  );
}

export default Camera;