import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from "react-webcam";

function MLCamera() {
  const [capture, setCapture] = useState(false);

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
        ? <Webcam height="200px" className="WebCam"/>
        : null
      }
      <br />
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