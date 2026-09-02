import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  RotateCcw,
} from "lucide-react";

function ResultCard({ result, onAnalyzeAnother }) {
  if (!result) return null;

  const getResultDetails = () => {
    const prediction = result.prediction.toLowerCase();

    if (prediction.includes("healthy")) {
      return {
        icon: <CheckCircle size={42} />,
        statusClass: "healthy-result",
        title: "Healthy Potato Leaf",
      };
    }

    if (prediction.includes("early")) {
      return {
        icon: <AlertTriangle size={42} />,
        statusClass: "early-result",
        title: "Early Blight Detected",
      };
    }

    return {
      icon: <XCircle size={42} />,
      statusClass: "late-result",
      title: "Late Blight Detected",
    };
  };

  const details = getResultDetails();

  return (
    <div className="result-card">
      <div className={`result-status ${details.statusClass}`}>
        {details.icon}
      </div>

      <div className="result-content">
        <span className="result-label">Classification Result</span>

        <h2>{details.title}</h2>

        <p className="result-explanation">
          {result.explanation}
        </p>

        <div className="confidence-section">
          <div className="confidence-header">
            <span>Confidence</span>
            <strong>{result.confidence}%</strong>
          </div>

          <div className="confidence-track">
            <div
              className={`confidence-fill ${details.statusClass}`}
              style={{ width: `${result.confidence}%` }}
            ></div>
          </div>
        </div>

        <button
          className="secondary-button"
          onClick={onAnalyzeAnother}
        >
          <RotateCcw size={18} />
          Analyze Another Leaf
        </button>
      </div>
    </div>
  );
}

export default ResultCard;