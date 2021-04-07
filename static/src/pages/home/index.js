import React from 'react'
import Alert from 'react-bootstrap/Alert'

const Home = () => {
  return (
    <Alert variant="success">
        <Alert.Heading>Machine Learning web app 💡</Alert.Heading>
        <p>A cool web app for machine learning, using <a href="https://reactjs.org/">React.js</a> to build the UI, and using <a href="https://palletsprojects.com/p/flask/">Flask</a> for the API.
        Most of the processing is distributed across threads by a task queue (<a href="https://docs.celeryproject.org/">Celery</a>), to obtain a more responsive UI.
        The broker used to mediate between clients and workers is a <a href="https://redis.io/">Redis</a> database.</p>
    </Alert>
  )
}

export default Home
