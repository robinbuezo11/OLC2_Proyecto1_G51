import React from "react";
import { useState, useRef, useEffect } from "react";
import Editor from "@monaco-editor/react";
import Results from "./components/Results";
import axios from "axios";
import Topbar from "../../components/common/Topbar";
import "../../styles/HomePage.css";
import { Alert, Button, Input, Tab, Tabs, Typography } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import * as d3 from 'd3';
import 'd3-graphviz';

const HomePage = () => {
    const [data, setData] = useState([['Consola']]);
    const [alert, setAlert] = useState(null);
    const inputFileRef = useRef(null);
    const [idEditor, setIdEditor] = useState(1);
    const [opDB, setOpDB] = useState(null);
    const [opOpen, setOpOpen] = useState(null);

    const [tabs, setTabs] = useState([
        { id: 1, label: "Query 1 ", code: "" },
    ]);
    const [activeTab, setActiveTab] = useState(tabs[0]);

    const handleTabChange = (event, newTab) => {
        setActiveTab(newTab);
    };

    const handleNewTab = () => {
        const newTab = { id: idEditor + 1, label: `Query ${idEditor + 1} `, code: "" };
        setTabs((prevTabs) => [...prevTabs, newTab]);
        setActiveTab(newTab);
        setIdEditor(idEditor + 1);
    };

    const handleCloseTab = (event, tabId) => {
        event.stopPropagation();
        if (tabs.length === 1) {
            handleEditorChange("");
            return;
        }
        tabs.forEach((tab, index) => {
            if (tab.id !== tabId) {
                setActiveTab(tabs[index]);
            }
        });
        setTabs((prevTabs) => prevTabs.filter((tab) => tab.id !== tabId));
    }

    const handleEditorChange = (newCode) => {
        setTabs((prevTabs) => 
            prevTabs.map((tab) => {
                if (tab.id === activeTab.id) {
                    tab = { ...tab, code: newCode };
                    setActiveTab(tab);
                    return tab;
                } else {
                    return tab
                }
            })
        );
    };
      

    const execute = () => {
        if (activeTab.label.includes('C3D')) {
            showMessage('error', 'No se puede ejecutar código C3D');
            return;
        }
        exec(activeTab.code);
    }
    const exec = (code) => {
        axios.post('http://localhost:4000/api/exec', {
            input: code
        })
        .then(function (response) {
            if (response.data.success) {
                if (response.data.result.length > 0) {
                    setData(response.data.result);
                } else {
                    setData([['Consola']]);
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    const manageDatabase = (e) => {
        e.preventDefault();
        if(opDB === 'create' || opDB === 'delete') {
            const dbName = document.getElementById('dbName').value;
            axios.post('http://localhost:4000/api/createDB', {
                dbName: dbName,
                action: opDB
            })
            .then(function (response) {
                closeModalDB();
                if (response.data.success) {
                    showMessage('success', response.data.message);
                } else {
                    showMessage('error', `${response.data.message}\n${response.data.error}`);
                }
            })
            .catch(function (error) {
                closeModalDB();
                showMessage('error', `${error}`);
            });
        } else if (opDB === 'select') {
            exec(`USE ${document.getElementById('dbName').value};`);
            closeModalDB();
        }
        setOpDB(null);
    }

    const generateAst = () => {
        axios.get('http://localhost:4000/api/getAst')
        .then(function (response) {
            if(response.data.success) {
                const dotCode = response.data.result;
                if(dotCode) {
                    generateGraph(dotCode, 'AST');
                } else {
                    showMessage('error', 'No se ha recibido el código dot');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        });
    }

    const generateSymbols = () => {
        axios.get('http://localhost:4000/api/getSymbols')
        .then(function (response) {
            if(response.data.success) {
                const dotCode = response.data.result;
                if(dotCode) {
                    generateGraph(dotCode, 'Tabla de Símbolos');
                } else {
                    showMessage('error', 'No se ha recibido el código dot');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        });
    }

    const generateError = () => {
        axios.get('http://localhost:4000/api/getError')
        .then(function (response) {
            if(response.data.success) {
                const dotCode = response.data.result;
                if(dotCode) {
                    generateGraph(dotCode, 'Errores');
                } else {
                    showMessage('error', 'No se ha recibido el código dot');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        });
    }

    const generateToken = () => {
        axios.get('http://localhost:4000/api/getToken')
        .then(function (response) {
            if(response.data.success) {
                const dotCode = response.data.result;
                if(dotCode) {
                    generateGraph(dotCode, 'Tokens');
                } else {
                    showMessage('error', 'No se ha recibido el código dot');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        });
    }

    const generateC3d = () => {
        if (activeTab.label.includes('C3D')) {
            showMessage('error', 'No se puede generar código C3D de código C3D');
            return;
        }
        axios.post('http://localhost:4000/api/getC3d', {
            input: activeTab.code
        })
        .then(function (response) {
            if(response.data.success) {
                const c3d = response.data.result;
                if(c3d) {
                    const newTab = { id: idEditor + 1, label: `C3D ${idEditor + 1} `, code: c3d };
                    setTabs((prevTabs) => [...prevTabs, newTab]);
                    setActiveTab(newTab);
                    setIdEditor(idEditor + 1);
                } else {
                    showMessage('error', 'No se ha recibido el código c3d');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        });
    }

    const getDump = () => {
        axios.get('http://localhost:4000/api/getDump')
        .then (function (response) {
            if(response.data.success) {
                const dump = response.data.result;
                if(dump) {
                    dowloadFile('dump.sql', dump);
                } else {
                    showMessage('error', 'No se ha recibido el dump');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {   
            showMessage('error', `${error}`);
        });
    }

    const getExport = () => {
        axios.get('http://localhost:4000/api/getExport')
        .then (function (response) {
            if(response.data.success) {
                const exportData = response.data.result;
                if(exportData) {
                    dowloadFile('export.sql', exportData);
                } else {
                    showMessage('error', 'No se ha recibido el export');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        });
    }       
    
    const importFile = () => {
        setOpOpen('import');
        inputFileRef.current.click();
    };

    const getTechDoc = () => {
        axios.get('http://localhost:4000/api/getTechDoc')
        .then (function (response) {
            if(response.data.success) {
                const doc = response.data.result;
                if(doc) {
                    openPdf(doc, 'Manual Técnico');
                } else {
                    showMessage('error', 'No se ha recibido el documento');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        }
        );
    }

    const getUserDoc = () => {
        axios.get('http://localhost:4000/api/getUserDoc')
        .then (function (response) {
            if(response.data.success) {
                const doc = response.data.result;
                if(doc) {
                    openPdf(doc, 'Manual de Usuario');
                } else {
                    showMessage('error', 'No se ha recibido el documento');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        }
        );
    }

    const getGrammar = () => {
        axios.get('http://localhost:4000/api/getGrammar')
        .then (function (response) {
            if(response.data.success) {
                const doc = response.data.result;
                if(doc) {
                    openPdf(doc, 'Gramática');
                } else {
                    showMessage('error', 'No se ha recibido el documento');
                }
            } else {
                showMessage('error', `${response.data.message}\n${response.data.error}`);
            }
        })
        .catch(function (error) {
            showMessage('error', `${error}`);
        }
        );
    }

    const openPdf = (pdfBase64, title) => {
        const newWindow = window.open('','_blank');
        newWindow.document.write(`<html><head><title>${title}</title></head><body><embed width="100%" height="100%" src="data:application/pdf;base64,${pdfBase64}" type="application/pdf"></body></html>`);
        newWindow.document.close();
    }

    function generateGraph(dotCode, title) {
        const newWindow = window.open('','_blank');
        newWindow.document.write(`<html><head><title>${title}</title></head><body><div id="graph"></div></body></html>`);
        newWindow.document.close();

        d3.select(newWindow.document.getElementById('graph')).graphviz().scale(1).width(newWindow.document.getElementById('graph').clientWidth).renderDot(dotCode);
    }

    const newFile = () => {
        handleEditorChange("");
    }

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            if (opOpen === 'open') {
                handleEditorChange(e.target.result);
                setOpOpen(null);   
            } else {
                exec(e.target.result);
            }
        };
        reader.readAsText(file);
    };
    const openFile = () => {
        setOpOpen('open');
        inputFileRef.current.click();
    };

    const saveFile = () => {
        dowloadFile('query.sql', activeTab.code);
    };

    const dowloadFile = (filename, text) => {
        const element = document.createElement("a");
        const file = new Blob([text], {type: 'text/plain'});
        element.href = URL.createObjectURL(file);
        element.download = filename;
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
        setOpDB('create');
    }

    const openModalDBDel = () => {
        openModalDB();
        setOpDB('delete');
    }

    const openModalDBSel = () => {
        openModalDB();
        setOpDB('select');
    }

    const closeModalDB = () => {
        document.getElementById('createdb').style.display = 'none';
        document.getElementById('formdb').reset();
        document.getElementById('overlay').style.display = 'none';
        setOpDB(null);
    }

    function showMessage(type, message) {
        document.getElementById('overlay').style.display = 'block';
        setAlert(<Alert
                    severity={type}
                    style={{position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 1000}}
                    >
                    {message}
                </Alert>);
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
        'dropDB': openModalDBDel,
        'newQuery': handleNewTab,
        'executeQuery': execute,
        'ast': generateAst,
        'symbols': generateSymbols,
        'errors': generateError,
        'tokens': generateToken,
        'c3d': generateC3d,
        'tech': getTechDoc,
        'createDump': getDump,
        'export': getExport,
        'import': importFile,
        'selectDB': openModalDBSel,
        'user': getUserDoc,
        'grammar': getGrammar,
    }

    return (
        <>
            {alert}
            <Topbar props={funcs}/>
            <div className="App">
                <div className='Content'>
                    <div className="editor1">
                        <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable" scrollButtons sx={{ minHeight: '6vh', height: '6vh'}}>
                            {tabs.map((tab) => (
                                <Tab 
                                    key={tab.id} 
                                    value={tab} 
                                    label={
                                        <span>
                                            {tab.label}
                                            <CloseIcon 
                                                fontSize="small" 
                                                onClick={(event) => handleCloseTab(event, tab.id)} 
                                                color="error" 
                                                style={{ paddingTop: '8px'}}/>
                                        </span>
                                    } 
                                />
                            ))}
                        </Tabs>
                        <Editor
                            height="54vh"
                            theme="vs-dark"
                            defaultLanguage='sql'
                            value={activeTab.code}
                            onChange={handleEditorChange}
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