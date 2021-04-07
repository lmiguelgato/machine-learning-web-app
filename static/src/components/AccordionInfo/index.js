import React from 'react'
import Accordion from 'react-bootstrap/Accordion'
import CardInfo from './card-info'

const AccordionInfo = () => {
  return (
  <>
    <Accordion>
      <CardInfo
        header='What is the difference between options 🕙, 📈, and 💾?'
        eventKey="0">
        🕙 optimizes the model for low latency. <br/>
        📈 optimizes the model for high accuracy. <br/>
        💾 optimizes the model for low memory usage. <br/>
        <em> If more than one option is selected,
        the model will try to optimize each metric when possible. <br/>
        If none is selected, the default training settings will be used.</em>
      </CardInfo>
      <CardInfo
        header='Why my model takes so long to train?'
        eventKey="1">
        If the model training is slower that expected,then your machine is probably
        not optimized for <a href="https://en.wikipedia.org/wiki/Machine_learning">
        machine learning</a>.
      </CardInfo>
    </Accordion>
  </>
  )
}

export default AccordionInfo
