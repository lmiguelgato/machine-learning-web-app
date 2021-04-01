import { Navbar, NavbarBrand } from 'reactstrap';
import { Switch, Route, BrowserRouter } from "react-router-dom";
import Websocket from './components/Websocket';
import AccordionInfo from './components/AccordionInfo';
import { About, ChangeRoute } from './components/MenuItem';
import MLCamera from './components/MLCamera';
import Alert from 'react-bootstrap/Alert'
import './App.css';


function App() {
  return (
    
    <div className="App">
      <Navbar dark color="primary">
      <div className="container">
        <NavbarBrand href="/home">Machine Learning web app 💡</NavbarBrand>
        <ChangeRoute label='Webcam' link="/webcam"/>
        <ChangeRoute label='Rock/Paper/Scissors' link="/rock-paper-scissors"/>
        <About />
      </div>
      </Navbar>

      <BrowserRouter basename="">
        <Switch>
          <Route path="/home">
          <Alert variant="success">
            <Alert.Heading>Machine Learning web app 💡</Alert.Heading>
            <p>
            A cool web app for machine learning, using <a href="https://reactjs.org/">React.js</a> to build the UI, and using <a href="https://palletsprojects.com/p/flask/">Flask</a> for the API.
            Most of the processing is distributed across threads by a task queue (<a href="https://docs.celeryproject.org/">Celery</a>), to obtain a more responsive UI.
            The broker used to mediate between clients and workers is a <a href="https://redis.io/">Redis</a> database.
            </p>
          </Alert>
          </Route>  

          <Route path="/webcam">
            <MLCamera />
            <header className="App-header">
            <Websocket options={{0: '🕙', 1: '📈', 2: '💾'}} type="checkbox"/>
            </header>
            <AccordionInfo />
          </Route>

          <Route path="/rock-paper-scissors">
            <MLCamera />
            <header className="App-header">
            <Websocket options={{0: '✊', 1: '✋', 2: '✌️'}} type="radio"/>
            </header>
            <AccordionInfo />
          </Route>
        </Switch> 
      </BrowserRouter>
    </div>
  );
}

export default App;
