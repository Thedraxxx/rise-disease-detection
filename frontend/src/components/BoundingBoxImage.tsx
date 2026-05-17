import { useEffect, useRef } from "react";
import "./BoundingBoxImage.css";

interface Props {
  preview: string;
  bbox: [number, number, number, number];
  disease: string;
  confidence: number;
}

const BoundingBoxImage = ({ preview, bbox, disease, confidence }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const image = imageRef.current;
    const canvas = canvasRef.current;
    if (!image || !canvas) return;

    const drawBox = () => {
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      // match canvas size to image display size
      canvas.width = image.clientWidth;
      canvas.height = image.clientHeight;

      // scale bbox coordinates to match displayed image size
      const scaleX = image.clientWidth / image.naturalWidth;
      const scaleY = image.clientHeight / image.naturalHeight;

      const [x, y, w, h] = bbox;
      const scaledX = x * scaleX;
      const scaledY = y * scaleY;
      const scaledW = w * scaleX;
      const scaledH = h * scaleY;

      // draw rectangle
      ctx.strokeStyle = "#e05a2b";
      ctx.lineWidth = 2;
      ctx.strokeRect(scaledX, scaledY, scaledW, scaledH);

      // draw label background
      const label = `${disease} · ${Math.round(confidence * 100)}%`;
      ctx.font = "500 12px Inter";
      const textWidth = ctx.measureText(label).width;
      ctx.fillStyle = "#e05a2b";
      ctx.fillRect(scaledX, scaledY - 22, textWidth + 16, 22);

      // draw label text
      ctx.fillStyle = "#ffffff";
      ctx.fillText(label, scaledX + 8, scaledY - 7);
    };

    if (image.complete) {
      drawBox();
    } else {
      image.onload = drawBox;
    }
  }, [preview, bbox, disease, confidence]);

  return (
    <div className="bbox-container">
      <img
        ref={imageRef}
        src={preview}
        alt="detection"
        className="bbox-image"
      />
      <canvas ref={canvasRef} className="bbox-canvas" />
    </div>
  );
};

export default BoundingBoxImage;