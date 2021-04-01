import { Navbar, NavbarBrand } from 'reactstrap';
import { Switch, Route, BrowserRouter } from "react-router-dom";
import Websocket from './components/Websocket';
import AccordionInfo from './components/AccordionInfo';
import { About, ChangeRoute } from './components/MenuItem';
import MLCamera from './components/MLCamera';
import './App.css';


function App() {
  return (
    
    <div className="App">
      <Navbar dark color="primary">
      <div className="container">
        <NavbarBrand href="/">Machine Learning web app</NavbarBrand>
        <ChangeRoute label='Webcam' link="/webcam"/>
        <About />
      </div>
      </Navbar>

      <BrowserRouter basename="">
        <Switch>
          <Route path="/webcam">
            <MLCamera />
            <header className="App-header">
            <Websocket />
            </header>
          </Route>
        </Switch> 
      </BrowserRouter>

      
      <AccordionInfo />
    </div>
  );
}

export default App;
