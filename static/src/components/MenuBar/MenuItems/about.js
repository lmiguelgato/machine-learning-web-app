import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'

const About = () => {
  const [show, setShow] = useState(false)
  return (
      <>
        <Alert show={show} variant="success">
          <p>
            A cool web app for machine learning, using  <a href="https://reactjs.org/">React.js</a> to build the UI and using <a href="https://flask.palletsprojects.com/">Flask</a> for the API.
            The original repo can be found <Alert.Link href="https://github.com/lmiguelgato/machine-learning-web-app">here</Alert.Link>.
          </p>
          <hr />
          <div className="d-flex justify-content-end">
              <Button onClick={() => setShow(false)} variant="outline-success">
                  Got it
              </Button>
          </div>
        </Alert>

        {!show && <Button onClick={() => setShow(true)}>About ...</Button>}
      </>
  )
}

export default About
