import { useState } from "react";
import { usePredict } from "../hooks/usePredict";
import ImageUploader from "../components/ImageUploader";
import ResultSection from "../components/ResultSection";
import "./Home.css";

const Home = () => {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const { isLoading, isError, predict, result } = usePredict();

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = () => {
    if (!image) return;
    predict(image);
  };

  return (
    <div className="home">
      <header className="header">
        <div className="logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M12 2a9 9 0 0 1 9 9c0 4-2.5 7.5-6 9" />
            <path d="M3 11a9 9 0 0 0 9 9" />
            <circle cx="12" cy="11" r="3" />
          </svg>
        </div>
        <h1 className="logo-text">RiceGuard</h1>
        <span className="tagline">Rice Disease Detection System</span>
      </header>

      <main className="main">
        <section className="upload-section">
          <p className="section-label">Upload Leaf Image</p>
          <ImageUploader
            preview={preview}
            onChange={handleImageChange}
          />
        </section>

        <button
          className="submit-btn"
          onClick={handleSubmit}
          disabled={!image || isLoading}
        >
          {isLoading ? "Analyzing..." : "Analyze Disease"}
        </button>

        {isError && (
          <div className="error-banner">
            {isError}
          </div>
        )}

        {result && (
          <ResultSection
            result={result}
            preview={preview!}
          />
        )}
      </main>
    </div>
  );
};

export default Home;