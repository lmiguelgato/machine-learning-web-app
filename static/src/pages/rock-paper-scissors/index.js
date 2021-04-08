import React, { useState } from 'react'
import MLCamera from '../../components/MLCamera/index'
import RadioButton from '../../components/RadioButton'

const RockPaperScissors = (props) => {
  const initialNumImages = () => {
    const initNumImages = []
    for (let i = 0; i < Object.keys(props.options).length; i++) {
      initNumImages.push(0)
    }
    return initNumImages
  }

  const [numImages, setNumImages] = useState(initialNumImages())
  const [, setRendering] = useState(false)

  const incrementCount = (select) => {
    const newNumImages = numImages
    newNumImages[select] += 1
    setNumImages(newNumImages)
    setRendering(prev => !prev)
  }

  return (
    <>
      <MLCamera
        screenshotFormat="image/jpeg"
        height="200px"
        endpoint={props.endpoint}
        select={props.select}
        onCapture={incrementCount}/>
      <br />
      <RadioButton
        optionDescription={props.options}
        option={props.select}
        setOption={props.setSelect}/>
      <br />
      {numImages[0] + ' -- ' + numImages[1] + ' -- ' + numImages[2]}
    </>
  )
}

export default RockPaperScissors
