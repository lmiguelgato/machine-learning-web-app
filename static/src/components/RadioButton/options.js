import React from 'react'
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup'
import ToggleButton from 'react-bootstrap/ToggleButton'

const Options = (props) => {
  const handleChange = (val) => props.setOption(val)

  return (
    <>
      { props.option > 0
        ? 'Take a picture when you are ready!'
        : 'Please, pick an option:'
      }
      <br/>
      <ToggleButtonGroup name="options" value={props.option} type="radio" onChange={handleChange}>
        {Object.keys(props.optionDescription).map((key) => {
          return (
            <ToggleButton
              key={key}
              disabled={props.isLoading}
              variant="outline-success"
              size="sm"
              value={key + 1}>
              { props.optionDescription[key] }
            </ToggleButton>
          )
        })}
      </ToggleButtonGroup>
    </>
  )
}

export default Options
