import React, { useState } from 'react';
import axios from "axios";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// Custom Message Box Component
const MessageBox = ({ message, type, onClose }) => {
  if (!message) return null;

  const typeClasses = {
    error: 'bg-red-500 text-white',
    success: 'bg-green-500 text-white',
    info: 'bg-blue-500 text-white',
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 animate-fade-in">
      <div className={`p-6 rounded-lg shadow-xl w-full max-w-sm relative transform transition-all duration-300 scale-100 ${typeClasses[type] || 'bg-gray-800 text-white'}`}>
        <p className="text-lg font-semibold mb-4">{message}</p>
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-white hover:text-gray-200 focus:outline-none"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>
  );
};

const App = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState(null);
  const [messageType, setMessageType] = useState('info');

  // Q&A states
  const [chatHistory, setChatHistory] = useState([]);
  const [question, setQuestion] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  const showMessage = (msg, type = 'info') => {
    setMessage(msg);
    setMessageType(type);
  };

  const closeMessage = () => setMessage(null);

  const handleUpload = async () => {
    if (!file) return showMessage("Please upload an audio file.", 'error');

    setLoading(true);
    setResult(null);
    setChatHistory([]); // reset chat on new upload
    closeMessage();

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 120000,
      });
      setResult(res.data);
      showMessage("Lecture summarized successfully!", 'success');
    } catch (error) {
      const errorMsg = error.response?.data?.error || "Processing failed, please try again.";
      showMessage(errorMsg, 'error');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setChatLoading(true);

    try {
      const res = await axios.post("http://localhost:5000/ask", { question });
      setChatHistory(res.data.history); // full conversation returned
      setQuestion('');
    } catch (error) {
      const errorMsg = error.response?.data?.error || "Failed to get answer.";
      showMessage(errorMsg, 'error');
      console.error(error);
    } finally {
      setChatLoading(false);
    }
  };

  const resetForm = () => {
    setFile(null);
    setResult(null);
    setChatHistory([]);
    closeMessage();
  };

  const handleCopy = (text) => {
    if (text) {
      navigator.clipboard.writeText(text).then(() => {
        showMessage('Copied to clipboard!', 'success');
      }).catch(() => {
        showMessage('Failed to copy.', 'error');
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 text-white font-inter flex flex-col items-center p-4">
      <MessageBox message={message} type={messageType} onClose={closeMessage} />

      {/* Upload Section */}
      <div className="bg-gray-800 bg-opacity-70 backdrop-blur-md p-8 sm:p-12 rounded-3xl shadow-2xl max-w-3xl w-full text-center space-y-8 border border-gray-700 animate-fade-in-up">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
          🧠 AI Lecture Summary
        </h1>
        <p className="text-gray-300 text-lg sm:text-xl leading-relaxed">
          Upload your lecture audio to get instant transcripts & intelligent summaries.
        </p>

        {/* Audio Upload */}
        <div className="relative border-2 border-dashed border-purple-500 rounded-xl p-6 sm:p-8 hover:border-purple-400 transition-colors duration-300 bg-gray-700 w-full mt-8">
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => setFile(e.target.files[0])}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          {file ? (
            <p className="text-lg text-green-300 font-semibold flex items-center justify-center">
              Selected: {file.name}
            </p>
          ) : (
            <p className="text-lg text-gray-400 flex items-center justify-center">
              Drag & Drop or Click to Upload Audio File
            </p>
          )}
        </div>

        {/* Action Button */}
        <button
          onClick={handleUpload}
          disabled={loading || !file}
          className="w-full sm:w-auto mt-8 px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold text-xl rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 ease-in-out focus:outline-none focus:ring-4 focus:ring-purple-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Processing...' : "Upload & Analyze"}
        </button>

        {loading && (
          <div className="mt-6 text-gray-400 text-lg animate-pulse">
            Processing audio... This may take a few minutes for longer lectures.
          </div>
        )}
      </div>

      {/* Result Section */}
      {result && (
        <div className="mt-10 w-full space-y-8 animate-fade-in px-2 sm:px-6 lg:px-12">
          {/* Transcript */}
          <section className="bg-gray-700 p-6 rounded-2xl shadow-xl border border-gray-600 w-full">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-3xl font-bold text-purple-300 flex items-center">
                <span className="mr-3">📝</span> Transcript
              </h2>
              <button
                onClick={() => handleCopy(result.transcript)}
                className="px-4 py-2 bg-gray-600 text-sm rounded-lg hover:bg-gray-500 transition-colors duration-200 flex items-center"
              >
                Copy
              </button>
            </div>
            <div className="bg-gray-900 p-4 rounded-lg border border-gray-700 max-h-[500px] overflow-y-auto text-gray-200 text-base leading-relaxed w-full">
              <pre className="whitespace-pre-wrap font-sans">{result.transcript}</pre>
            </div>
          </section>

          {/* AI Summary */}
          <section className="bg-gray-700 p-6 rounded-2xl shadow-xl border border-gray-600 w-full">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-3xl font-bold text-pink-300 flex items-center">
                <span className="mr-3">🧠</span> AI Summary
              </h2>
              <button
                onClick={() => handleCopy(result.analysis)}
                className="px-4 py-2 bg-gray-600 text-sm rounded-lg hover:bg-gray-500 transition-colors duration-200 flex items-center"
              >
                Copy
              </button>
            </div>
            <div className="bg-gray-900 p-4 rounded-lg border border-gray-700 max-h-[500px] overflow-y-auto text-gray-200 text-base leading-relaxed w-full">
              <ReactMarkdown
                children={result.analysis}
                remarkPlugins={[remarkGfm]}
                components={{
                  p: ({ node, ...props }) => <p className="mb-2 text-base leading-relaxed" {...props} />,
                  li: ({ node, ...props }) => <li className="ml-5 list-disc mb-1" {...props} />,
                  strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
                }}
              />
            </div>
          </section>

          {/* Q&A Chatbot */}
          <section className="bg-gray-700 p-6 rounded-2xl shadow-xl border border-gray-600 w-full">
            <h2 className="text-3xl font-bold text-green-300 mb-4 flex items-center">
              <span className="mr-3">💬</span> Q&A Chatbot
            </h2>

            {/* Chat Messages */}
            <div className="bg-gray-900 p-4 rounded-lg border border-gray-700 max-h-[400px] overflow-y-auto space-y-4">
              {chatHistory.length === 0 && (
                <p className="text-gray-400">Start asking questions about the lecture...</p>
              )}
              {chatHistory.map((msg, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg max-w-3xl ${
                    msg.role === 'user' ? 'bg-purple-600 ml-auto text-right' : 'bg-gray-800 mr-auto text-left'
                  }`}
                >
                  <ReactMarkdown
                    children={msg.content}
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({ node, ...props }) => <p className="mb-2 text-base leading-relaxed" {...props} />,
                      li: ({ node, ...props }) => <li className="ml-5 list-disc mb-1" {...props} />,
                      strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
                    }}
                  />
                </div>
              ))}
            </div>

            {/* Input box */}
            <div className="mt-4 flex gap-2">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about the lecture..."
                className="flex-1 p-3 rounded-lg border border-gray-600 bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button
                onClick={handleAsk}
                disabled={chatLoading || !question.trim()}
                className="px-6 py-3 bg-purple-600 rounded-lg font-bold hover:bg-purple-500 transition-all disabled:opacity-50"
              >
                {chatLoading ? '...' : 'Ask'}
              </button>
            </div>
          </section>
        </div>
      )}
    </div>
  );
};

export default App;
