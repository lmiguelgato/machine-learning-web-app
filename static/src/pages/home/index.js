import React from 'react'
import CardInfo from './card-info'
import Accordion from 'react-bootstrap/Accordion'

const Home = () => {
  return (
    <>
      <br />
      <p>
        A cool web app for machine learning, using  <a href="https://reactjs.org/">React.js</a> to build the UI and using <a href="https://flask.palletsprojects.com/">Flask</a> for the API.
      </p>

      <Accordion>
        <CardInfo
          header='How are computationally heavy tasks handled?'
          eventKey="1">
          Most of the processing is distributed across threads by a <a href="https://docs.celeryproject.org/">Celery</a> task queue, to obtain a more responsive UI. The broker used to mediate between clients and workers is a <a href="https://redis.io/">Redis</a> database.
        </CardInfo>
        <CardInfo
          header='How do the server and the client communicate with each other?'
          eventKey="2">
          Server and clients are synced regarding the status of a task through low latency bi-directional communications using <a href="https://flask-socketio.readthedocs.io/">Flask-SocketIO</a>.
        </CardInfo>
        <CardInfo
          header='Is this project optimized for deployment?'
          eventKey="3">
          The API implements a machine learning model server, which is a quick and easy implementation for demonstration projects, where a Flask endpoint handles inference. However, this is not how I would recommend to deploy machine learning models to production endpoints. For multiple reasons, this simplified approach is inflexible and inefficient:
          <br />
          - backend code and machine learning code live on the same codebase,
          <br />
          - there is no model version control,
          <br />
          - inference requests are not handled in batches, but sequentially as they arrive.
          <br />
          <br />
          To address these issues, the recommended approach is to serve the model using well-established tools like <a href="https://www.tensorflow.org/tfx/guide/serving/">TensorFlow Serving</a>, which can be deployed in a separate Docker container.
        </CardInfo>
      </Accordion>
    </>
  )
}

export default Home
