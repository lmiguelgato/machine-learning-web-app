import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from "react-webcam";
import * as tf from '@tensorflow/tfjs';

function MLCamera(props) {
  const [capture, setCapture] = useState(false);
  const [batchedImage, setBatchedImage] = useState(tf.tensor([[[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]]]));

  const webcamRef = React.useRef(null);

  const takePicture = React.useCallback(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
      console.log(imageSrc)
      //const tensorImage = tf.browser.fromPixels(imageSrc);
      //const reversedImage = tensorImage.reverse(1);
      //const croppedImage = cropImage(reversedImage);
      //setBatchedImage(croppedImage.expandDims(0).toFloat().div(tf.scalar(127)).sub(tf.scalar(1)));
    },
    [webcamRef]
  );

  const cropImage = (img) => {
    const size = Math.min(img.shape[0], img.shape[1]);
    const centerHeight = img.shape[0] / 2;
    const beginHeight = centerHeight - (size / 2);
    const centerWidth = img.shape[1] / 2;
    const beginWidth = centerWidth - (size / 2);
    return img.slice([beginHeight, beginWidth, 0], [size, size, 3]);
  }

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