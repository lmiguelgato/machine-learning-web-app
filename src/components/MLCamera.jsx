import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from "react-webcam";
import axios from 'axios';

const ENDPOINT = 'http://127.0.0.1:5000/';  // TODO: define ENDPOINT only once


function MLCamera() {
  const [capture, setCapture] = useState(false);

  const webcamRef = React.useRef(null);

  const takePicture = React.useCallback(
    async () => {
      const imageSrc = webcamRef.current.getScreenshot();

      const api_response = await axios.post(
        ENDPOINT + 'capture',
        {data_uri: imageSrc}
      );
      console.log(api_response)
    },
    [webcamRef]
  );

  const toggleOnOff = () => {
      if (capture) {
        setCapture(false)
      } else {
        setCapture(true)
      }
  }

  return (
    <>
      { capture
        ? <>
          <Webcam audio={false}
            screenshotFormat="image/jpeg"
            ref={webcamRef}
            height="200px"
            className="WebCam"
          />
          </>
        : null
      }
      <br />      
      { capture 
          ? <Button
              variant="success"
              size="sm"
              onClick={takePicture}
              className="Button">
              📷 Capture
            </Button>
          : null
      }
      <Button className="Button"
      variant="success"
      size="sm"
      onClick={toggleOnOff}>
      { capture ? '⛔ Turn off webcam' : '🎥 Turn on webcam' }
      </Button>
    </>
  );
}

export default MLCamera;