import React, { useState } from 'react';
import 'bulma/css/bulma.min.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  const generateContent = async () => {
    setLoading(true);
    const input = document.querySelector("#input").value;
    const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ input_text: input })
    });
    const data = await response.json();
    setContent(data.generated_content);
    setLoading(false);
  };

  return (
    <div className="container is-fluid">
      <section className="hero is-info">
        <div className="hero-body">
          <p className="title">
            AI Content Generator
          </p>
          <p className="subtitle">
            Create amazing content instantly with AI
          </p>
        </div>
      </section>

      <div className="section">
        <div className="columns">
          <div className="column is-half is-offset-one-quarter">
            <div className="box">
              <label className="label">Enter your prompt</label>
              <textarea
                id="input"
                className="textarea"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Type a prompt like 'Create a blog post on AI in healthcare'"
              ></textarea>
              <button
                className={`button is-primary is-fullwidth ${loading ? 'is-loading' : ''}`}
                onClick={generateContent}
                disabled={loading}
                style={{ marginTop: '15px' }}
              >
                {loading ? "Generating..." : "Generate Content"}
              </button>
            </div>

            {content && (
              <div className="box">
                <h2 className="title is-4">Generated Content</h2>
                <p className="content">{content}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
