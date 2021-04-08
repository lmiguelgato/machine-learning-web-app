import React, { useState } from 'react'
import MLCamera from '../../components/MLCamera/index'
import RadioButton from '../../components/RadioButton'

const RockPaperScissors = (props) => {
  const initNumImages = []
  for (let i = 0; i < Object.keys(props.options).length; i++) {
    initNumImages.push(0)
  }
  const numImages = useState(initNumImages)

  return (
    <>
      <MLCamera
        screenshotFormat="image/jpeg"
        height="200px"
        endpoint={props.endpoint}
        select={props.select}/>
      <br />
      <RadioButton
        optionDescription={props.options}
        option={props.select}
        setOption={props.setSelect}/>
      <br />
      {numImages[0][0] + ' -- ' + numImages[0][1] + ' -- ' + numImages[0][2]}
    </>
  )
}

export default RockPaperScissors
