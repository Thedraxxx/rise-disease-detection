
import ModelCard from "./ModelCard";
import BoundingBoxImage from "./BoundingBoxImage";
import "./ResultSection.css";
import type { PredictionResult } from "../services/api";

interface Props {
  result: PredictionResult
  preview: string;
}

const ResultSection = ({ result, preview }: Props) => {
  return (
    <div className="result">

      <section className="result__section">
        <p className="result__label">Model Comparison</p>
        <div className="result__cards">
          <ModelCard
            name="CNN"
            disease={result.results.cnn.disease}
            confidence={result.results.cnn.confidence}
            isBest={result.best_model === "cnn"}
          />
          <ModelCard
            name="ResNet-50"
            disease={result.results.resnet.disease}
            confidence={result.results.resnet.confidence}
            isBest={result.best_model === "resnet"}
          />
          <ModelCard
            name="YOLOv8"
            disease={result.results.yolo.disease}
            confidence={result.results.yolo.confidence}
            isBest={result.best_model === "yolo"}
          />
        </div>
      </section>

      {result.results.yolo.bbox && (
        <section className="result__section">
          <p className="result__label">YOLOv8 Detection</p>
          <BoundingBoxImage
            preview={preview}
            bbox={result.results.yolo.bbox}
            disease={result.results.yolo.disease}
            confidence={result.results.yolo.confidence}
          />
        </section>
      )}

      <section className="result__section">
        <p className="result__label">Disease Information</p>
        <div className="result__info">
          <h2 className="result__disease">{result.disease}</h2>
          <p className="result__description">{result.description}</p>
          <p className="result__treatment-label">Recommended Treatment</p>
          <p className="result__treatment">{result.treatment}</p>
        </div>
      </section>

    </div>
  );
};

export default ResultSection;