import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from 'react-webcam'
import axios from 'axios'

const Camera = (props) => {
  const [capture, setCapture] = useState(false)
  const [isPredicting, setIsPredicting] = useState(false)
  const [predictionStatus, setPredictionStatus] = useState('')

  const webcamRef = React.useRef(null)

  const togglePredict = () => {
    setIsPredicting(!isPredicting)

    if (isPredicting) {
      setPredictionStatus('')
    } else {
      setPredictionStatus('Prediction ...')
    }
    /* while (isPredicting) {
      setStatus(s => s + ' + Prediction ...')
    } */
    /*
    const apiResponse = await axios.post(
      TRAIN_ROUTE,
      {
        user_id: userId,
        dataset_up_to_date: false // TODO get this from actual state
      }
    ) */
  }

  const takePicture = React.useCallback(
    async () => {
      if (props.select !== undefined && props.select >= 0) {
        const imageSrc = webcamRef.current.getScreenshot()
        if (imageSrc !== null) {
          await axios.post(
            props.endpoint,
            {
              data_uri: imageSrc,
              screenshot_format: props.screenshotFormat,
              selected: props.select[0]
            }
          )
        } else {
          toggleOnOff()
        }
      }
    }, [webcamRef, props.select, props.screenshotFormat, props.endpoint])

  const toggleOnOff = () => {
    if (capture) {
      setCapture(false)
      setIsPredicting(false)
      setPredictionStatus('')
    } else {
      setCapture(true)
    }
  }

  return (
      <>
        <br />
        { capture
          ? <>
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
                className="Button"
                disabled={props.select < 0}>
                📷 Capture
              </Button>
              <Button
                variant="success"
                size="sm"
                onClick={togglePredict}
                className="Button">
                { isPredicting ? '🚫 Stop model' : '🦾 Run model' }
              </Button>
            </>
          : 'Ready to start? Turn on the camera and allow this app to use it.'
        }
        <Button
            className="Button"
            variant="success"
            size="sm"
            onClick={toggleOnOff}>
            { capture ? '⛔ OFF' : '🎥 ON' }
        </Button>
        <br />
        { capture
          ? predictionStatus
          : null
        }
      </>
  )
}

export default Camera
