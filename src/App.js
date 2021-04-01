import { Navbar, NavbarBrand } from 'reactstrap';
import './App.css';
import Websocket from './components/Websocket';
import AccordionInfo from './components/AccordionInfo';
import Info from './components/Info';


function App() {
  return (
    <div className="App">
      <Navbar dark color="primary">
      <div className="container">
        <NavbarBrand href="/">Awesome web app using React and Flask.</NavbarBrand>
        <Info />
      </div>
      </Navbar>
      <header className="App-header">        
        <Websocket />        
      </header>
      <AccordionInfo />
    </div>
  );
}

export default App;
