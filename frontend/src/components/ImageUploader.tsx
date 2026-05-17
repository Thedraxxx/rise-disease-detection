import "./ImageUploader.css";

interface Props {
  preview: string | null;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const ImageUploader = ({ preview, onChange }: Props) => {
  return (
    <div className="uploader">
      {!preview ? (
        <label className="upload-area">
          <input
            type="file"
            accept="image/jpg,image/jpeg,image/png,image/webp"
            onChange={onChange}
            className="file-input"
          />
          <div className="upload-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
          </div>
          <p className="upload-title">Drop your rice leaf image here</p>
          <p className="upload-sub">or click to browse · JPG, PNG, WEBP up to 10MB</p>
        </label>
      ) : (
        <div className="preview-wrap">
          <img src={preview} alt="preview" className="preview-img" />
          <span className="preview-label">Preview</span>
          <label className="change-btn">
            <input
              type="file"
              accept="image/jpg,image/jpeg,image/png,image/webp"
              onChange={onChange}
              className="file-input"
            />
            Change Image
          </label>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;