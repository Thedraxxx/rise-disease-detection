import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/api";

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
});

export interface ModelResult {
  confidence: number;
  disease: string;
  bbox?: [number, number, number, number];
}
export interface PredictionResult {
  disease: string;
  best_model: string;
  description: string;
  treatment: string;

  results: {
    cnn: ModelResult;
    resnet: ModelResult;
    yolo: ModelResult;
  };
}
interface ApiResponse<T> {
  data: T;
  message: string;
  status: "success" | "error";
}

export const predictDisease = async (imageFile: File): Promise<PredictionResult> => {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await apiClient.post<ApiResponse<PredictionResult>>("/predict", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  if(response.data.status === "error"){
    throw new Error(response.data.message)
  }
  return response.data.data
};
