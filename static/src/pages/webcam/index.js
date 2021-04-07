import React from 'react'
import MLCamera from '../../components/MLCamera/index'
import AccordionInfo from '../../components/AccordionInfo/index'

const WebCam = (props) => {
  return (
    <>
      <MLCamera
        screenshotFormat="image/jpeg"
        height="200px"
        endpoint={props.endpoint}/>
      { props.children }
      <AccordionInfo />
    </>
  )
}

export default WebCam
