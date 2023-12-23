import React from "react";
import { useState, useRef, useEffect } from "react";
import Editor from "@monaco-editor/react";
import Results from "./components/Results";
import axios from "axios";
import Topbar from "../../components/common/Topbar";
import "../../styles/HomePage.css";
import { Alert, Button, Input, Typography } from "@mui/material";

const HomePage = () => {
    const data = [
        ['id', 'name', 'age', 'address', 'salary', 'join_date'],
        [1, 'Paul', 32, 'California', 20000, '2018-01-25'],
        [2, 'Allen', 25, 'Texas', 15000, '2018-01-25'],
        [3, 'Teddy', 23, 'Norway', 20000, '2018-01-25'],
        [4, 'Mark', 25, 'Rich-Mond', 65000, '2018-01-25'],
        [5, 'David', 27, 'Texas', 85000, '2018-01-25'],
        [6, 'Kim', 22, 'South-Hall', 45000, '2018-01-25'],
        [7, 'James', 24, 'Houston', 10000, '2018-01-25']
    ]

    const [code, setCode] = useState('');
    const [alert, setAlert] = useState(null);
    const inputFileRef = useRef(null);
    let opDB = null;
    const options = {
    };

    const execute = () => {
        axios.post('http://localhost:4000/api/exec', {
            input: code
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    const newFile = () => {
        setCode('');
    }

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            setCode(e.target.result);
        };
        reader.readAsText(file);
    };
    const openFile = () => {
        inputFileRef.current.click();
    };

    const saveFile = () => {
        const element = document.createElement("a");
        const file = new Blob([code], {type: 'text/plain'});
        element.href = URL.createObjectURL(file);
        element.download = "code.sql";
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
        document.body.removeChild(element);
        URL.revokeObjectURL(element.href);
    };

    const close = () => {
        window.location.reload(true);
    }

    const openModalDB = () => {
        document.getElementById('createdb').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        opDB = 'create';
    }

    const openModalDBDel = () => {
        openModalDB();
        opDB = 'delete';
    }

    const closeModalDB = () => {
        document.getElementById('createdb').style.display = 'none';
        document.getElementById('formdb').reset();
        document.getElementById('overlay').style.display = 'none';
        opDB = null;
    }

    const manageDatabase = (e) => {
        e.preventDefault();
        const dbName = document.getElementById('dbName').value;
        axios.post('http://localhost:4000/api/createDB', {
            dbName: dbName,
            action: opDB
        })
        .then(function (response) {
            closeModalDB();
            if (response.data.success) {
                document.getElementById('overlay').style.display = 'block';
                setAlert(<Alert 
                            severity="success" 
                            style={{position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 1000}}
                            >
                            {`${response.data.message}`}
                        </Alert>);
            } else {
                document.getElementById('overlay').style.display = 'block';
                setAlert(<Alert 
                            severity="error" 
                            style={{position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 1000}}
                            >
                            {`${response.data.message}\n${response.data.error}`}
                        </Alert>);
            }
        })
        .catch(function (error) {
            closeModalDB();
            document.getElementById('overlay').style.display = 'block';
            setAlert(<Alert 
                        severity="error" 
                        style={{position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 1000}}
                        >
                        {`${error}`}
                    </Alert>);
        });
    }

    useEffect(() => {
        if (alert) {
            const timer = setTimeout(() => {
                setAlert(null);
                document.getElementById('overlay').style.display = 'none';
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [alert]);

    const funcs = {
        'execute': execute, 
        'new': newFile,
        'open': openFile,
        'save': saveFile,
        'close': close,
        'createDB': openModalDB,
        'dropDB': openModalDBDel
    }

    return (
        <>
            {alert}
            <Topbar props={funcs}/>
            <div className="App">
                <div className='Content'>
                    <div className="editor1">
                    <Editor
                        height="55vh"
                        theme="vs-dark"
                        defaultLanguage='sql'
                        value={code}
                        options={options}
                        onChange={setCode}
                    />
                    </div>
                </div>
            </div>
            <div className='Results'>
                <Results data={data} />
            </div>
            <input type="file" ref={inputFileRef} style={{display: 'none'}} onChange={handleFileChange} accept=".sql, .xsql" />
            <div id="overlay"></div>
            <div id="createdb">
                <form id="formdb" onSubmit={manageDatabase}>
                    <Typography variant="h6">
                        Base de Datos    
                    </Typography>
                    <Input type="text" id="dbName" placeholder="Nombre" required/>
                    <br/>
                    <Button type="button" variant="contained" color="error" style={{margin: '15px'}} onClick={closeModalDB}>Cancelar</Button>
                    <Button type="submit" variant="contained" color="primary" style={{margin: '15px'}}>Aceptar</Button>
                </form>
            </div>
        </>
    );
};

export default HomePage;