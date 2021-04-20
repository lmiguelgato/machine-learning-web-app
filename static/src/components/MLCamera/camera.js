import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Webcam from 'react-webcam'
import axios from 'axios'

// Constants
import { PREDICT_ROUTE, CONFUSED_EMOJIS } from '../../constant'

const Camera = (props) => {
  const [capture, setCapture] = useState(false)
  const [isPredicting, setIsPredicting] = useState(false)
  const [predictionStatus, setPredictionStatus] = useState('')

  const webcamRef = React.useRef(null)

  const togglePredict = async () => {
    setIsPredicting(!isPredicting)

    if (isPredicting) {
      setPredictionStatus('')
    } else {
      setPredictionStatus('I am ')
      const imageSrc = webcamRef.current.getScreenshot()

      const apiResponse = await axios.post(
        PREDICT_ROUTE,
        {
          data_uri: imageSrc
        }
      )

      const roundPercent = Math.round(apiResponse.data.probability * 100)
      console.log(roundPercent)
      if (roundPercent > 50) {
        const inference = props.optionDescription[apiResponse.data.label]
        setPredictionStatus(s => s + roundPercent + ' % confident it is a ' + inference)
      } else {
        setPredictionStatus(s => s + '... ' + CONFUSED_EMOJIS[Math.floor(Math.random() * CONFUSED_EMOJIS.length)] + ' ... not sure what that is.')
      }
    }
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
