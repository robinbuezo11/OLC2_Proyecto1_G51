import '../styles/Dashboard.css';
import  { useState, useRef} from 'react';
import { saveAs } from 'file-saver';
import Editor from '@monaco-editor/react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import axios from 'axios';

function App() {
  const [code, setCode] = useState('');
  const [resultado, setResultado] = useState('');
  const navDropdownRef = useRef(null);

  const options = {
  };

  function analizar(){
    axios.post('http://localhost:5000/analyzer', {
      input: code
    })
    .then(function (response) {
      console.log(response);
      if(response.data.errors.length > 0){
        setResultado(response.data.result + '\n' + '--- Se encontraron errores en el código ---');
      }else{
        setResultado(response.data.result);
      }
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  function graphAST(){
    axios.get('http://localhost:5000/graphAST')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  function generateSymbols(){
    axios.get('http://localhost:5000/generateSymbols')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  function generateErrors(){
    axios.get('http://localhost:5000/generateErrors')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  function open(){
    let win = window.open('http://localhost:3000/', '_blank');
    win.focus();
  }

  function save(){
    const blob = new Blob([code], {type: 'text/plain;charset=utf-8'});
    saveAs(blob, 'file.tw');
  }

  function read(e){
    const file = e.target.files[0];
    if (!file) return;
    const fileReader = new FileReader();

    fileReader.readAsText(file);
    fileReader.onload = () => {
      setCode('');
      setCode(fileReader.result);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
      <Navbar bg="secondary" variant='dark' id='navbar'>
      <Container id='cont-nav'>
        <Nav id='nav' className="me-auto">
          <NavDropdown className='navitm' title="Archivo" id="basic-nav-dropdown" ref={navDropdownRef}>
            <NavDropdown.Item onClick={()=>{open()}}>Crear</NavDropdown.Item>
            <label id='openinput'>
                <input
                  id='fileinput'
                  type='file'
                  accept='.tw'
                  style={{display: 'none'}}
                  multiple={false}
                  onChange={(e)=>{
                    read(e);
                    navDropdownRef.current.querySelector('.dropdown-menu').classList.remove('show');
                    document.getElementById('fileinput').value = '';
                  }}>
                </input>
                <span id='openbt'>Abrir</span>
            </label>
            <NavDropdown.Item onClick={()=>{save()}}>Guardar</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown className='navitm' title="Reportes" id="basic-nav-dropdown">
            <NavDropdown.Item onClick={()=>{graphAST()}}>Árbol AST</NavDropdown.Item>
            <NavDropdown.Item onClick={()=>{generateSymbols()}}>Tabla de Símbolos</NavDropdown.Item>
            <NavDropdown.Item onClick={()=>{generateErrors()}}>Tabla de Errores</NavDropdown.Item>
          </NavDropdown>
          <Nav.Link className='navitm' onClick={()=>{analizar()} }>Ejecutar</Nav.Link>
        </Nav>
      </Container>
      </Navbar>
      </header>
      <div className='Content'>
        <div className="editor1">
          <Editor
            height="70vh"
            theme="vs-dark"
            defaultLanguage='sql'
            value={code}
            options={options}
            onChange={setCode}
          />
        </div>
      </div>
    </div>
  );
}

export default App;