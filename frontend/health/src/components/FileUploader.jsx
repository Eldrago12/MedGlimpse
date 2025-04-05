import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadPDFs } from "../utils/api";
import { CloudArrowUpIcon } from "@heroicons/react/24/outline"; // npm install @heroicons/react

function FileUploader({ onUploadSuccess }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setSelectedFiles(
      Array.from(event.target.files)
        .filter((file) => file.type === "application/pdf")
        .slice(0, 3),
    );
  };

  const handleUpload = async () => {
    if (selectedFiles.length > 0) {
      setIsLoading(true);
      const formData = new FormData();
      selectedFiles.forEach((file) => formData.append("pdfs", file));

      try {
        const data = await uploadPDFs(formData);
        setIsLoading(false);
        onUploadSuccess(data.response, data.session_id);
        navigate("/");
      } catch (error) {
        setIsLoading(false);
        console.error("Upload error:", error);
      }
    } else {
      alert("Please select PDF files to upload.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center gap-6 text-center">
      <CloudArrowUpIcon className="w-16 h-16 text-primary animate-bounce" />
      <h1 className="text-3xl font-semibold text-white">
        Upload Your Health Reports
      </h1>
      <p className="text-gray-300">Select up to 3 PDF files for analysis.</p>
      <div className="relative w-full max-w-md">
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          accept=".pdf"
          className="appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-primary focus:ring-1 sm:text-sm bg-transparent text-white"
        />
        {selectedFiles.length > 0 && (
          <div className="mt-2 text-sm text-gray-400">
            Selected files: {selectedFiles.map((file) => file.name).join(", ")}
          </div>
        )}
      </div>
      <button
        onClick={handleUpload}
        disabled={isLoading}
        className="bg-primary hover:bg-secondary text-white font-semibold py-3 px-6 rounded-full shadow-md transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
      >
        {isLoading ? "Analyzing..." : "Analyze Reports"}
      </button>
    </div>
  );
}

export default FileUploader;
