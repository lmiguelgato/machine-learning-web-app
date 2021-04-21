import React from 'react'
import Alert from 'react-bootstrap/Alert'

const Home = () => {
  return (
    <Alert variant="success">
      <Alert.Heading>About ...</Alert.Heading>
      <p>A cool web app for machine learning, using  <a href="https://reactjs.org/">React.js</a> to build the UI and using <a href="https://flask.palletsprojects.com/">React.js</a> for the API.
        <br />
        <br />
        Most of the processing is distributed across threads by a task queue <a href="https://docs.celeryproject.org/">Celery</a>, to obtain a more responsive UI. The broker used to mediate between clients and workers is a <a href="https://redis.io/">Redis</a> database.
        <br />
        <br />
        Although completely redesigned, the way asynchronous tasks are handled in this project is inspired by some example code from <a href="https://github.com/jwhelland/flask-socketio-celery-example/">this project</a>, which in turn is based on <a href="https://github.com/miguelgrinberg/flask-celery-example">this project</a>. In contrast with those, this project uses <a href="https://flask-socketio.readthedocs.io/">Flask-SocketIO</a> for low latency bi-directional communications between the clients and the server.
        <br />
        <br />
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
      </p>
    </Alert>
  )
}

export default Home
