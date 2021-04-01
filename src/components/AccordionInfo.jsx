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
            What is the difference between options 1, 2, and 3?
        </Accordion.Toggle>
        </Card.Header>
        <Accordion.Collapse eventKey="0">
        <Card.Body>
            <b>Option 1</b> optimizes the model for low latency. <br />
            <b>Option 2</b> optimizes the model for high accuracy. <br />
            <b>Option 3</b> optimizes the model for low memory usage. <br />
            <em>If more than one option is selected, the model will try to optimize each metric when possible.</em>
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