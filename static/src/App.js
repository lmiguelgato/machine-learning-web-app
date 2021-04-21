import React, { useState } from 'react'
import { Switch, Route, BrowserRouter } from 'react-router-dom'

// Pages
import Home from './pages/home'
import RockPaperScissors from './pages/rock-paper-scissors'

// Components
import MenuBar from './components/MenuBar'
import Websocket from './components/WebSocket/index'

// Styles
import './App.css'

// Constants
import { ENDPOINT, CAPTURE_ROUTE } from './constant'

function App () {
  const [select, setSelect] = useState(-1)

  return (
    <div className="App">
      <MenuBar/>

      <BrowserRouter basename="">
        <Switch>
          <Route exact path="/" component={Home} />

          <Route path="/rock-paper-scissors">
            <RockPaperScissors
              select={select}
              setSelect={setSelect}
              endpoint={CAPTURE_ROUTE}
              options={{ 0: '✊', 1: '✋', 2: '✌️' }} />
            <Websocket endpoint={ENDPOINT}/>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  )
}

export default App
