import React from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Accordion from 'react-bootstrap/Accordion';

function AccordionInfo() {
    return (
    <Accordion>
    <Card>
        <Card.Header>
        <Accordion.Toggle as={Button} variant="link" eventKey="0">
            What is the difference between options 🕙, 📈, and 💾?
        </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey="0">
        <Card.Body>
            🕙 optimizes the model for low latency. <br />
            📈 optimizes the model for high accuracy. <br />
            💾 optimizes the model for low memory usage. <br />
            <em>If more than one option is selected, the model will try to optimize each metric when possible.<br />If none is selected, the default training settings will be used.</em>
        </Card.Body>
        </Accordion.Collapse>
    </Card>
    <Card>
        <Card.Header>
        <Accordion.Toggle as={Button} variant="link" eventKey="1">
            Why my model takes so long to train?
        </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey="1">
        <Card.Body>
            If the model training is slower that expected, then your machine is probably 
            not optimized for <a href="https://en.wikipedia.org/wiki/Machine_learning">machine learning</a>.
        </Card.Body>
        </Accordion.Collapse>
    </Card>
    </Accordion>
  );
}

export default AccordionInfo;