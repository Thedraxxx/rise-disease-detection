import { useState } from "react";
import { predictDisease, type PredictionResult } from "../services/api";

export const usePredict = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);

  const predict = async (imageFile: File) => {
    setIsLoading(true);
    setIsError(null);
    setResult(null);
    try {
      const data = await predictDisease(imageFile);
      setResult(data);
    } catch (error: any) {
      const status = error.response?.status;
       const serverMessage = error.response?.data?.message;

      if (status === 413) {
        setIsError(serverMessage || "Image is too large. Please upload an image under 10MB.");
      } else if (status === 400) {
        setIsError(serverMessage || "Invalid image. Please upload a JPG, PNG or WEBP file.");
      } else if (status === 404) {
        setIsError(serverMessage ||
          "Prediction endpoint not found. Check if backend is running.",
        );
      } else if (status === 422) {
        setIsError(serverMessage || "Could not process the image. Please try a different one.");
      } else if (status === 429) {
        setIsError(serverMessage || "Too many requests. Please wait a moment and try again.");
      } else if (status === 500) {
        setIsError(serverMessage || "Server error. Something went wrong on our end.");
      } else if (status === 503) {
        setIsError(serverMessage || "Server is unavailable. Please try again later.");
      } else if (error.code === "ECONNABORTED") {
        setIsError(serverMessage ||
          "Request timed out. The model is taking too long to respond.",
        );
      } else if (error.code === "ERR_NETWORK") {
        setIsError(
         serverMessage || "Cannot connect to server. Make sure the backend is running.",
        );
      } else {
        setIsError(serverMessage || "Failed to analyze image. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isError,
    result,
    isLoading,
    predict,
  };
};
