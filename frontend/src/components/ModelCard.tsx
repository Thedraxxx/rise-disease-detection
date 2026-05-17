import "./ModelCard.css";

interface Props {
  name: string;
  disease: string;
  confidence: number;   
  isBest: boolean;
}

const ModelCard = ({ name, disease, confidence, isBest }: Props) => {
  return (
    <div className={`model-card ${isBest ? "model-card--best" : ""}`}>
      <div className="model-card__header">
        <span className="model-card__name">{name}</span>
        {isBest && <span className="model-card__badge">Best</span>}
      </div>
      <p className="model-card__disease">{disease}</p>
      <div className="model-card__bar">
        <div
          className="model-card__fill"
          style={{ width: `${Math.round(confidence * 100)}%` }}
        />
      </div>
      <span className="model-card__conf">
        {Math.round(confidence * 100)}% confidence
      </span>
    </div>
  );
};

export default ModelCard;

