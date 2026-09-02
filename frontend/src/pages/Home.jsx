import { Link } from "react-router-dom";
import { ScanLine, Leaf, History } from "lucide-react";

function Home() {
  return (
    <div className="page">
      <section className="hero">
        <div className="hero-content">
          <span className="eyebrow">
            <Leaf size={16} />
            Potatoe Leaf Inspection
          </span>

          <h1>
            Potato Leaf
            <br />
            <span>Classification</span>
          </h1>

          <p>
            Upload a potato leaf image and get an instant
            classification with confidence and a simple explanation.
          </p>

          <Link to="/analyze" className="primary-button">
            <ScanLine size={20} />
            Analyze the Leaf
          </Link>
        </div>

        <div className="hero-card">
          <Leaf size={100} strokeWidth={1} />

          <h3>Ready for inspection</h3>

          <p>
            Upload an image to begin analyzing your potato leaf.
          </p>
        </div>
      </section>

      <section className="feature-grid">
        <div className="feature-card">
          <ScanLine size={24} />
          <h3>Instant Analysis</h3>
          <p>
            Upload an image a
          </p>
        </div>

        <div className="feature-card">
          <Leaf size={24} />
          <h3>Clear Results</h3>
          <p>
            View the predicted disease or healthy status with confidence.
          </p>
        </div>

        <div className="feature-card">
          <History size={24} />
          <h3>Inspection History</h3>
          <p>
            Keep track of previous potato leaf inspections in one place.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Home;