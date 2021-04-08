import React, { useState } from 'react'
import axios from 'axios'
import MLCamera from '../../components/MLCamera/index'
import RadioButton from '../../components/RadioButton'

const RockPaperScissors = (props) => {
  const ENDPOINT = 'http://127.0.0.1:5000' // TODO: get from a global scope

  async function getStorage () {
    const res = await axios.post(
      ENDPOINT + '/storage', { }
    )
    return res
  }

  const initialNumImages = () => {
    const initNumImages = []
    const storage = getStorage()
    console.log(storage)
    for (let i = 0; i < Object.keys(props.options).length; i++) {
      // initNumImages.push(storage[String(i)].length)
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
      {numImages[0] + '+ || ' + numImages[1] + '+ ||  ' + numImages[2] + '+ '}
    </>
  )
}

export default RockPaperScissors
