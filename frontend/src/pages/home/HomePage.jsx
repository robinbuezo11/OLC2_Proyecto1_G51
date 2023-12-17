import React from "react";
import { useState } from "react";
import Editor from "@monaco-editor/react";

const HomePage = () => {
    const [code, setCode] = useState('');
    const options = {
    };

    return (
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
    );
};

export default HomePage;