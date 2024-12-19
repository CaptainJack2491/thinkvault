// Import necessary dependencies
import React, { useState } from 'react';
import './App.css'; // Optional: Add some styling here

function App() {
    // State variables for link, thoughts, and response
    const [link, setLink] = useState('');
    const [thoughts, setThoughts] = useState('');
    const [response, setResponse] = useState(null);

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Prepare data to send to the backend
        const data = { link, thoughts };

        try {
            // Send data to the backend via POST request
            const res = await fetch('http://127.0.0.1:5000/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            // Parse the response from the backend
            const result = await res.json();
            setResponse(result.message);
        } catch (error) {
            console.error('Error:', error);
            setResponse('An error occurred while processing your request.');
        }
    };

    return (
        <div className="App">
            <h1>Transcript Summarizer</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="link">Enter the video/article link:</label>
                    <input
                        type="text"
                        id="link"
                        value={link}
                        onChange={(e) => setLink(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="thoughts">Enter your thoughts:</label>
                    <textarea
                        id="thoughts"
                        value={thoughts}
                        onChange={(e) => setThoughts(e.target.value)}
                        required
                    ></textarea>
                </div>
                <button type="submit">Submit</button>
            </form>

            {response && <div className="response">{response}</div>}
        </div>
    );
}

export default App;
