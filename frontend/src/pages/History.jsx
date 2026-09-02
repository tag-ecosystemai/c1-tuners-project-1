import { useEffect, useState } from "react";
import { History as HistoryIcon } from "lucide-react";
import HistoryCard from "../components/HistoryCard";

function History() {
  const [inspections, setInspections] = useState([]);

  useEffect(() => {
    const savedInspections =
      JSON.parse(localStorage.getItem("potatoInspections")) || [];

    setInspections(savedInspections);
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Inspection History</h1>

        <p>
          View your previous potato leaf classifications.
        </p>
      </div>

      {inspections.length === 0 ? (
        <div className="empty-state">
          <HistoryIcon size={48} />

          <h2>No inspections yet</h2>

          <p>
            Your completed potato leaf analyses will appear here.
          </p>
        </div>
      ) : (
        <div className="history-grid">
          {inspections.map((inspection) => (
            <HistoryCard
              key={inspection.id}
              inspection={inspection}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default History;