import React from 'react'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Accordion from 'react-bootstrap/Accordion'

const CardInfo = (props) => {
  return (
    <Card>
      <Card.Header>
        <Accordion.Toggle as={Button} variant="link" eventKey={props.eventKey}>
          {props.header}
        </Accordion.Toggle>
      </Card.Header>

      <Accordion.Collapse eventKey={props.eventKey}>
        <Card.Body>
          {props.children}
          </Card.Body>
      </Accordion.Collapse>
    </Card>
  )
}

export default CardInfo
