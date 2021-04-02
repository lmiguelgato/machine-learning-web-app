import React from 'react';
import { Switch, Route, BrowserRouter } from "react-router-dom";

// Pages
import Home from './pages/home'
import WebCam from './pages/webcam'
import RockPaperScissors from './pages/rock-paper-scissors'

// Components
import MenuBar from './components/MenuBar'
import Websocket from './components/WebSocket/index';

// Styles
import './App.css';

const ENDPOINT = 'http://127.0.0.1:5000/';  // TODO: define ENDPOINT only once


function App() {
  return (
    
    <div className="App">
      <MenuBar/>

      <BrowserRouter basename="">
        <Switch>
          <Route path="/home">
            <Home/>
          </Route>

          <Route path="/webcam">
            <WebCam endpoint={ENDPOINT}>
              <header className="App-header">
                <Websocket endpoint={ENDPOINT} options={{0: '🕙', 1: '📈', 2: '💾'}} type="checkbox"/>
              </header>
            </WebCam>
          </Route>

          <Route path="/rock-paper-scissors">
            <RockPaperScissors endpoint={ENDPOINT}>
              <header className="App-header">
              {/* nRocks + ' -- ' + nPapers + ' -- ' + nScissors */}
              <Websocket endpoint={ENDPOINT} options={{0: '✊', 1: '✋', 2: '✌️'}} type="radio"/>
              </header>
            </RockPaperScissors>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
