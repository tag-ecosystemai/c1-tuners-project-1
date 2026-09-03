import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  RotateCcw,
  ShieldCheck,
  Info,
  Camera,
} from "lucide-react";

function ResultCard({ result, onAnalyzeAnother }) {
  if (!result) return null;

  const confidence = Number(result.confidence);
  const prediction = result.prediction.toLowerCase();

  // Determine disease status
  const getResultDetails = () => {
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

  // Confidence-aware explanation
  const getConfidenceExplanation = () => {
    if (confidence >= 85) {
      return {
        level: "High Confidence",
        message: `The AI is highly confident in this ${result.prediction} classification based on the visual patterns detected in the uploaded leaf image.`,
      };
    }

    if (confidence >= 60) {
      return {
        level: "Moderate Confidence",
        message: `The AI detected patterns associated with ${result.prediction}, but the result has moderate confidence. A clearer image may help provide additional verification.`,
      };
    }

    return {
      level: "Low Confidence",
      message:
        "The AI is not sufficiently confident in this classification. Try uploading another clear image with good lighting and the leaf clearly visible.",
    };
  };

  // Confidence-aware recommendation
  const getRecommendation = () => {
    // LOW CONFIDENCE
    if (confidence < 60) {
      return {
        title: "Recommended Next Step",
        message:
          "Retake the image in good lighting. Ensure the potato leaf is clearly visible, in focus, and occupies most of the image.",
        icon: <Camera size={22} />,
      };
    }

    // HEALTHY
    if (prediction.includes("healthy")) {
      return {
        title: "Recommendation",
        message:
          "The leaf appears healthy. Continue monitoring your potato plants regularly and inspect them for new symptoms.",
        icon: <ShieldCheck size={22} />,
      };
    }

    // MEDIUM CONFIDENCE DISEASE
    if (confidence < 85) {
      return {
        title: "Recommendation",
        message:
          "The AI detected possible disease symptoms, but additional verification is recommended. Upload another image or inspect more leaves.",
        icon: <Info size={22} />,
      };
    }

    // HIGH CONFIDENCE DISEASE
    return {
      title: "Recommendation",
      message:
        "The AI strongly detected disease-related patterns. Inspect nearby plants and consider consulting an agricultural expert for confirmation and appropriate treatment.",
      icon: <AlertTriangle size={22} />,
    };
  };

  const details = getResultDetails();
  const confidenceInfo = getConfidenceExplanation();
  const recommendation = getRecommendation();

  return (
    <div className="result-card">
      <div className={`result-status ${details.statusClass}`}>
        {details.icon}
      </div>

      <div className="result-content">
        <span className="result-label">Classification Result</span>

        <h2>{details.title}</h2>

        {/* MODEL EXPLANATION */}
        {result.explanation && (
          <p className="result-explanation">
            {result.explanation}
          </p>
        )}

        {/* CONFIDENCE */}
        <div className="confidence-section">
          <div className="confidence-header">
            <span>Confidence</span>
            <strong>{confidence.toFixed(1)}%</strong>
          </div>

          <div className="confidence-track">
            <div
              className={`confidence-fill ${details.statusClass}`}
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>

        {/* CONFIDENCE-AWARE EXPLANATION */}
        <div className="confidence-info">
          <div className="info-title">
            <ShieldCheck size={20} />
            <strong>{confidenceInfo.level}</strong>
          </div>

          <p>{confidenceInfo.message}</p>
        </div>

        {/* CONFIDENCE-AWARE RECOMMENDATION */}
        <div className="recommendation-card">
          <div className="recommendation-title">
            {recommendation.icon}
            <strong>{recommendation.title}</strong>
          </div>

          <p>{recommendation.message}</p>
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