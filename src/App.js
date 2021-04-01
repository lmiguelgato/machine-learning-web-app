import { Navbar, NavbarBrand } from 'reactstrap';
import './App.css';
import Websocket from './components/Websocket';
import AccordionInfo from './components/AccordionInfo';
import Info from './components/Info';
import MLCamera from './components/MLCamera';


function App() {
  return (
    <div className="App">
      <Navbar dark color="primary">
      <div className="container">
        <NavbarBrand href="/">Machine Learning web app</NavbarBrand>
        <Info />
      </div>
      </Navbar>
      <MLCamera />
      <header className="App-header">
        <Websocket />
      </header>
      <AccordionInfo />
    </div>
  );
}

export default App;
