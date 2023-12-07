import '../styles/Dashboard.css';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';
import MonacoEditor from 'react-monaco-editor';
import axios from 'axios';
import { Link } from 'react-router-dom';


function Dashboard() {
  const [code, setCode] = useState('');
  const [result, setResult] = useState('');
  const hiddenFileInput = React.useRef(null);

  function executeCommand(command) {
    axios.post('http://18.117.141.89:8000/api/command', {
      command: command
    }).then((response) => {
      if(response.data.status === 'success') {
        setResult(response.data.result);
      } else {
        setResult(response.data.error);
      }
    }).catch((error) => {
      alert(error);
    });
  }

  function handleChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();

    reader.readAsText(file);
    reader.onload = () => {
      setCode(reader.result);
    }
  }

  return (
    <div className="Dashboard">
      <div className='Dashboard-header'>
        <Button variant="primary" onClick={() => executeCommand(code)} className='Ejecutar'>Ejecutar</Button>
        <Button variant="secondary" onClick={() => hiddenFileInput.current.click()} className='Abrir'>Abrir Archivo</Button>
        <Link className='Link-login' to='/login'>
          <Button variant="success" className='login'>Login</Button>
        </Link>
        <input
          type="file"
          ref={hiddenFileInput}
          onChange={handleChange}
          accept='.mia'
          style={{ display: 'none' }}
        />
      </div>
      <div className='Title'>
        <h1>Comandos</h1>
      </div>
      <div className='Code'>
        <MonacoEditor
          className={'CodeEditor'}
          language="shell"
          value={code}
          options={{ minimap: { enabled: false } }}
          onChange={setCode}
        />
      </div>
      <div className='Title'>
        <h1>Consola</h1>
      </div>
      <div className='Result'>
        <MonacoEditor
          language="shell"
          theme={'vs-dark'}
          value={result}
          options={{ minimap: { enabled: false } }}
          onChange={setResult}
        />
      </div>
    </div>
  );
}

export default Dashboard;