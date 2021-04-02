import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from "react-webcam";


function MLCamera() {
  const [capture, setCapture] = useState(false);

  const webcamRef = React.useRef(null);

  const takePicture = React.useCallback(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
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