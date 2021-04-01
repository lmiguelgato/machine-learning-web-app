import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert'

function Info() {
    const [show, setShow] = useState(false);

  return (
    <>
      <Alert show={show} variant="success">
        <p>
          This is just a template web app using React JS to build the UI, and Flask as API. It uses Redis and celery to handle background tasks.
          The original repo can be found <Alert.Link href="https://github.com/lmiguelgato/react-flask-template">here</Alert.Link>.
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
  );
}

export default Info;