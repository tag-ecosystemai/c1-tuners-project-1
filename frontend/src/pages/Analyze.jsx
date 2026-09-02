import { useState } from "react";
import {
  Upload,
  Image as ImageIcon,
  X,
  ScanLine,
  AlertCircle,
  LoaderCircle,
} from "lucide-react";

import ResultCard from "../components/ResultCard";

function Analyze() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  // Handle image selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setError("");
    setResult(null);

    if (!file) return;

    // Validating that the selected file is an image
    if (!file.type.startsWith("image/")) {
      setError("Please select a valid image file.");
      return;
    }

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  };

  // Remove the selected image
  const removeImage = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError("");
  };

  // Analyze the selected image
  const handleAnalyze = () => {
    if (!selectedFile) {
      setError("Please upload a potato leaf image first.");
      return;
    }

    setIsAnalyzing(true);
    setResult(null);
    setError("");

    // TEMPORARY MOCK AI ANALYSIS
    // This will later be replaced with the FastAPI backend request.
    setTimeout(() => {
      const mockResult = {
        prediction: "Early Blight",
        confidence: 94.7,
        explanation:
          "The AI detected visual patterns associated with early blight on the potato leaf.",
      };

      // Create a new inspection record
      const newInspection = {
        id: Date.now(),
        image: preview,
        prediction: mockResult.prediction,
        confidence: mockResult.confidence,
        explanation: mockResult.explanation,
        date: new Date().toLocaleString(),
      };

      // Get existing inspection history
      const existingInspections =
        JSON.parse(localStorage.getItem("potatoInspections")) || [];

      // Save the new inspection at the beginning of the history
      localStorage.setItem(
        "potatoInspections",
        JSON.stringify([newInspection, ...existingInspections])
      );

      // Display the result
      setResult(mockResult);
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Analyze Potato Leaf</h1>

        <p>
          Upload a clear image of a potato leaf for AI-powered classification.
        </p>
      </div>

      <div className="analyze-layout">
        {/* LEFT SIDE - IMAGE UPLOAD AND RESULTS */}
        <div className="upload-container">
          {!preview ? (
            <label className="upload-box">
              <div className="upload-icon">
                <Upload size={32} />
              </div>

              <h2>Upload your leaf image</h2>

              <p>Click here to browse and select an image</p>

              <span>Supported formats: JPG, JPEG, PNG</span>

              <div className="primary-button">
                <Upload size={18} />
                Choose Image
              </div>

              <input
                type="file"
                accept="image/png, image/jpeg, image/jpg"
                onChange={handleFileChange}
                hidden
              />
            </label>
          ) : (
            <div className="image-preview-container">
              <img
                src={preview}
                alt="Selected potato leaf"
                className="image-preview"
              />

              {!isAnalyzing && (
                <button
                  className="remove-image-button"
                  onClick={removeImage}
                  title="Remove image"
                >
                  <X size={20} />
                </button>
              )}

              <div className="image-info">
                <ImageIcon size={18} />
                <span>{selectedFile?.name}</span>
              </div>
            </div>
          )}

          {/* ERROR MESSAGE */}
          {error && (
            <div className="error-message">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          {/* ANALYZE BUTTON */}
          {selectedFile && !result && (
            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? (
                <>
                  <LoaderCircle className="spinner" size={20} />
                  Analyzing Leaf...
                </>
              ) : (
                <>
                  <ScanLine size={20} />
                  Analyze Leaf
                </>
              )}
            </button>
          )}

          {/* RESULT CARD */}
          {result && (
            <ResultCard
              result={result}
              onAnalyzeAnother={removeImage}
            />
          )}
        </div>

        {/* RIGHT SIDE - INFORMATION */}
        {!result && (
          <div className="analysis-info-card">
            <h3>What can it detect?</h3>

            <div className="disease-list">
              <div>
                <span className="status healthy"></span>
                Healthy
              </div>

              <div>
                <span className="status early"></span>
                Early Blight
              </div>

              <div>
                <span className="status late"></span>
                Late Blight
              </div>
            </div>

            <p>
              Upload a clear and well-lit image of a potato leaf for the best
              classification result.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Analyze;