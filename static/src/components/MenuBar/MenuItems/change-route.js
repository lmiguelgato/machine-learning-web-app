import React from 'react'
import Button from 'react-bootstrap/Button'

const ChangeRoute = (props) => {
  return (
      <Button href={props.link}>{props.label}</Button>
  )
}

export default ChangeRoute
