import React, { useState } from "react";
import "./UploadPDF.css";

export default function UploadPDF() {
  const [file, setFile] = useState(null);
  const [jsonOutput, setJsonOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF");

    setLoading(true);
    setJsonOutput(null);

    const formData = new FormData();
    formData.append("pdf", file);
    for (let pair of formData.entries()) {
        console.log(pair[0], pair[1]); // key, value
      }

    try {
      const response = await fetch("http://localhost:5000/process", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setJsonOutput(result);
    } catch (error) {
      alert("Error processing the file");
    }

    setLoading(false);
  };

  return (
    <div className="upload-card">
      <h2 className="title">Upload PDF & Show JSON Output</h2>

      <div className="upload-section">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="file-input"
        />
        <button className="upload-button" onClick={handleUpload}>
          Process PDF
        </button>
      </div>

      {loading && <p className="loading">Processing...</p>}

      {jsonOutput && (
        <pre className="json-output">
          {JSON.stringify(jsonOutput, null, 2)}
        </pre>
      )}
    </div>
  );
}
