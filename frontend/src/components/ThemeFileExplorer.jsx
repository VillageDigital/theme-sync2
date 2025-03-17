import React, { useState, useEffect } from "react";

function ThemeFileExplorer() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState("");

  // Fetch theme files from the backend
  useEffect(() => {
    fetch("/api/themes/files")
      .then((response) => response.json())
      .then((data) => setFiles(data.files))
      .catch((error) => console.error("Error fetching theme files:", error));
  }, []);

  // Fetch content when a file is selected
  const handleFileClick = (fileName) => {
    fetch(`/api/themes/file-content?file=${fileName}`)
      .then((response) => response.text())
      .then((content) => {
        setSelectedFile(fileName);
        setFileContent(content);
      })
      .catch((error) => console.error("Error loading file:", error));
  };

  return (
    <div className="theme-file-explorer">
      <h2>Theme File Explorer</h2>
      <div className="file-list">
        <ul>
          {files.map((file) => (
            <li key={file} onClick={() => handleFileClick(file)}>
              {file}
            </li>
          ))}
        </ul>
      </div>
      {selectedFile && (
        <div className="file-viewer">
          <h3>Viewing: {selectedFile}</h3>
          <pre>{fileContent}</pre>
        </div>
      )}
    </div>
  );
}

export default ThemeFileExplorer;
