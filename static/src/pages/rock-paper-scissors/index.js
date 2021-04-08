import React, { useEffect, useState } from 'react'
import axios from 'axios'
import MLCamera from '../../components/MLCamera/index'
import RadioButton from '../../components/RadioButton'

const RockPaperScissors = (props) => {
  const ENDPOINT = 'http://127.0.0.1:5000' // TODO: get from a global scope

  const [numImages, setNumImages] = useState([0, 0, 0])

  const getStorage = () => {
    return async () => {
      const res = await axios.post(
        ENDPOINT + '/storage', { }
      )

      const initNumImages = []
      for (let i = 0; i < Object.keys(res.data.storage).length; i++) {
        initNumImages.push(res.data.storage[String(i)].length)
      }
      setNumImages(initNumImages)
    }
  }

  useEffect(() => {
    return getStorage()
  })

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
      {numImages[0] + ' || ' + numImages[1] + ' ||  ' + numImages[2]}
    </>
  )
}

export default RockPaperScissors
