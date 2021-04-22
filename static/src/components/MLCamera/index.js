import React from 'react'
import Camera from './camera'

const MLCamera = (props) => {
  return (
    <Camera
      screenshotFormat={props.screenshotFormat}
      height={props.height}
      endpoint={props.endpoint}
      select={props.select}
      onCapture={props.onCapture}
      optionDescription={props.optionDescription}/>
  )
}

export default MLCamera
