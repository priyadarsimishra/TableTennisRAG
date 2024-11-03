import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [file, setFile] = useState(null);
    const [advice, setAdvice] = useState(null);

    useEffect(() => {
        return () => {
            if (file && file.preview) {
                console.log('Revoking URL:', file.preview);
                URL.revokeObjectURL(file.preview);
            }
        };
    }, [file]);

    const handleFileChange = (event) => {
        if (file && file.preview) {
            console.log('Revoking URL:', file.preview);
            URL.revokeObjectURL(file.preview);
        }
        const newFile = event.target.files[0];
        if (newFile) {
            newFile.preview = URL.createObjectURL(newFile);
            console.log('Creating URL:', newFile.preview);
            setFile(newFile);
        }
        setAdvice("get better");
    };

    return (
        <div className="App">
            <header className="App-header">
                <p>Upload ping pong video (MP4)</p>
                <input type="file" accept=".mp4" onChange={handleFileChange} />
                {file && file.type === 'video/mp4' && (
                    <video key={file.preview} width="320" height="240" controls>
                        <source src={file.preview} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                )}
                <p>{advice}</p>
            </header>
        </div>
    );
}

export default App;