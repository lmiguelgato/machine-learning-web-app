import React from 'react'
import Options from './options'

const RadioButton = (props) => {
  return (
    <>
      <Options
        optionDescription={props.optionDescription}
        isLoading={props.isLoading}
        option={props.option}
        setOption={props.setOption}/>
    </>
  )
}

export default RadioButton
