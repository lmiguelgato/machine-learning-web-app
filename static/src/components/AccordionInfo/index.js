import React from 'react'
import Accordion from 'react-bootstrap/Accordion'
import CardInfo from './card-info'

const AccordionInfo = () => {
  return (
  <>
    <Accordion>
      <CardInfo
        header='Why my model takes so long to train?'
        eventKey="1">
        If the model training is slower that expected, then your machine is probably
        not optimized for <a href="https://en.wikipedia.org/wiki/Machine_learning">
        machine learning</a>.
      </CardInfo>
    </Accordion>
  </>
  )
}

export default AccordionInfo
