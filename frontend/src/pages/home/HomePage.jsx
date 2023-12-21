import React from "react";
import { useState, useRef } from "react";
import Editor from "@monaco-editor/react";
import Results from "./Results";
import axios from "axios";
import Topbar from "../../components/common/Topbar";
import "../../styles/HomePage.css";

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
    const inputFileRef = useRef(null);
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

    const funcs = {
        'execute': execute, 
        'new': newFile,
        'open': openFile,
        'save': saveFile,
        'close': close
    }

    return (
        <>
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
        </>
    );
};

export default HomePage;