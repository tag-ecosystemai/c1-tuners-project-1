import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  Calendar,
} from "lucide-react";

function HistoryCard({ inspection }) {
  const getStatusDetails = () => {
    const prediction = inspection.prediction.toLowerCase();

    if (prediction.includes("healthy")) {
      return {
        icon: <CheckCircle size={20} />,
        className: "healthy",
      };
    }

    if (prediction.includes("early")) {
      return {
        icon: <AlertTriangle size={20} />,
        className: "early",
      };
    }

    return {
      icon: <XCircle size={20} />,
      className: "late",
    };
  };

  const status = getStatusDetails();

  return (
    <div className="history-card">
      <div className="history-image-container">
        <img
          src={inspection.image}
          alt={inspection.prediction}
          className="history-image"
        />

        <div className={`history-status ${status.className}`}>
          {status.icon}
        </div>
      </div>

      <div className="history-card-content">
        <h3>{inspection.prediction}</h3>

        <div className="history-confidence">
          {inspection.confidence}% Confidence
        </div>

        <div className="history-date">
          <Calendar size={14} />
          {inspection.date}
        </div>
      </div>
    </div>
  );
}

export default HistoryCard;