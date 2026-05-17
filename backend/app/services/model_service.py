import os
import logging
from config import Config

logger = logging.getLogger(__name__)

class ModelService:

    def __init__(self):
        self.cnn_model = None
        self.resnet_model = None
        self.yolo_model = None
        self._load_models()

    def _load_models(self):
        """Load all models once at server startup."""
        logger.info("Loading models...")
        self.cnn_model    = self._load_cnn()
        self.resnet_model = self._load_resnet()
        self.yolo_model   = self._load_yolo()
        logger.info("All models loaded successfully.")

    def _load_cnn(self):
        path = os.path.join(Config.MODELS_FOLDER, "cnn_model.pt")
        if not os.path.exists(path):
            logger.warning("CNN model not found. Using mock.")
            return None
        # TODO: load actual model when .pt file is ready
        # import torch
        # return torch.load(path, map_location="cpu")
        return None

    def _load_resnet(self):
        path = os.path.join(Config.MODELS_FOLDER, "resnet_model.pt")
        if not os.path.exists(path):
            logger.warning("ResNet model not found. Using mock.")
            return None
        # TODO: load actual model when .pt file is ready
        # import torch
        # return torch.load(path, map_location="cpu")
        return None

    def _load_yolo(self):
        path = os.path.join(Config.MODELS_FOLDER, "yolov8_model.pt")
        if not os.path.exists(path):
            logger.warning("YOLOv8 model not found. Using mock.")
            return None
        # TODO: load actual model when .pt file is ready
        # from ultralytics import YOLO
        # return YOLO(path)
        return None

    def predict_all(self, image_path: str) -> dict:
        """Run all 3 models and return combined results."""
        cnn_result    = self._predict_cnn(image_path)
        resnet_result = self._predict_resnet(image_path)
        yolo_result   = self._predict_yolo(image_path)

        best_model = self._get_best_model(cnn_result, resnet_result, yolo_result)

        return {
            "cnn":        cnn_result,
            "resnet":     resnet_result,
            "yolo":       yolo_result,
            "best_model": best_model
        }

    def _predict_cnn(self, image_path: str) -> dict:
        if self.cnn_model is None:
            # Mock response until model is ready
            return {
                "disease":    "Leaf Blast",
                "confidence": 0.87
            }
        # TODO: real inference
        # tensor = preprocess(image_path)
        # output = self.cnn_model(tensor)
        # return parse_output(output)

    def _predict_resnet(self, image_path: str) -> dict:
        if self.resnet_model is None:
            # Mock response until model is ready
            return {
                "disease":    "Leaf Blast",
                "confidence": 0.93
            }
        # TODO: real inference

    def _predict_yolo(self, image_path: str) -> dict:
        if self.yolo_model is None:
            # Mock response until model is ready
            return {
                "disease":    "Leaf Blast",
                "confidence": 0.79,
                "bbox":       [148, 135, 95, 60]
            }
        # TODO: real inference

    def _get_best_model(self, cnn: dict, resnet: dict, yolo: dict) -> str:
        """Return the model name with highest confidence."""
        scores = {
            "cnn":    cnn["confidence"],
            "resnet": resnet["confidence"],
            "yolo":   yolo["confidence"]
        }
        return max(scores, key=scores.get)