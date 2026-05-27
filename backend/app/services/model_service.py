import os
import logging
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from config import Config

logger = logging.getLogger(__name__)

class CNN(nn.Module):
    def __init__(self, num_classes=3):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.pool(x)
        x = self.fc(x)
        return x


class ModelService:

    def __init__(self):
        self.cnn_model = None
        self.resnet_model = None
        self.yolo_model = None
        self._load_models()

    def _load_models(self):
        self.cnn_model    = self._load_cnn()
        self.resnet_model = self._load_resnet()
        self.yolo_model   = self._load_yolo()

    def _load_cnn(self):
        path = os.path.join(Config.MODELS_FOLDER, "cnn_model.pth")
        if not os.path.exists(path):
            print("CNN model not found. Using mock.")
            return None
        try:
            model = CNN()
            model.load_state_dict(torch.load(path, map_location="cpu"))
            model.eval()
            print("[DEBUG] CNN loaded successfully!")
            return model
        except Exception as e:
            print(f"[ERROR] Failed to load CNN: {e}")
            return None

    def _load_resnet(self):
        path = os.path.join(Config.MODELS_FOLDER, "resnet_model.pth")
        if not os.path.exists(path):
            print("ResNet model not found. Using mock.")
            return None
        try:
            model = models.resnet50(weights=None)
            num_ftrs = model.fc.in_features
            model.fc = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_ftrs, 3)
            )

            # friend saved full checkpoint not just weights
            checkpoint = torch.load(path, map_location="cpu")
            print("Checkpoint keys:", checkpoint.keys())
            model.load_state_dict(checkpoint["model_state_dict"])

            model.eval()
            print("[DEBUG] ResNet loaded successfully!")
            return model
        except Exception as e:
            print(f"[ERROR] Failed to load ResNet: {e}")
            return None

    def _load_yolo(self):
        path = os.path.join(Config.MODELS_FOLDER, "yolov8_model.pt")
        if not os.path.exists(path):
            print("YOLOv8 model not found. Using mock.")
            return None
        try:
            from ultralytics import YOLO
            print(f"[DEBUG] Loading YOLOv8 from {path}")
            model = YOLO(path)
            print("[DEBUG] YOLOv8 loaded successfully!")
            return model
        except Exception as e:
            print(f"[ERROR] Failed to load YOLOv8: {e}")
            return None

    def predict_all(self, image_path: str) -> dict:
        yolo_result = self._predict_yolo(image_path)

        # if YOLO finds nothing, skip CNN and ResNet
        if yolo_result["disease"] == "Unknown":
            return {
                "cnn":          {"disease": "N/A", "confidence": 0.0},
                "resnet":       {"disease": "N/A", "confidence": 0.0},
                "yolo":         yolo_result,
                "best_model":   "yolo",
                "not_relevant": True
            }

        cnn_result    = self._predict_cnn(image_path)
        resnet_result = self._predict_resnet(image_path)
        best_model    = self._get_best_model(cnn_result, resnet_result, yolo_result)

        return {
            "cnn":          cnn_result,
            "resnet":       resnet_result,
            "yolo":         yolo_result,
            "best_model":   best_model,
            "not_relevant": False
        }

    def _predict_cnn(self, image_path: str) -> dict:
        if self.cnn_model is None:
            return {"disease": "Brown Spot", "confidence": 0.87}

        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])

        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = self.cnn_model(tensor)
            probs = torch.softmax(output, dim=1)
            conf, idx = torch.max(probs, dim=1)

        classes = ["Bacterial Leaf Blight", "Brown Spot", "Leaf Smut"]
        return {
            "disease":    classes[idx.item()],
            "confidence": round(conf.item(), 4)
        }

    def _predict_resnet(self, image_path: str) -> dict:
        if self.resnet_model is None:
            return {"disease": "Brown Spot", "confidence": 0.45}

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = self.resnet_model(tensor)
            probs = torch.softmax(output, dim=1)
            conf, idx = torch.max(probs, dim=1)

        classes = ["Bacterial Leaf Blight", "Brown Spot", "Leaf Smut"]
        return {
            "disease":    classes[idx.item()],
            "confidence": round(conf.item(), 4)
        }

    def _predict_yolo(self, image_path: str) -> dict:
        if self.yolo_model is None:
            return {"disease": "Brown Spot", "confidence": 0.79, "bbox": [148, 135, 95, 60]}

        results = self.yolo_model(image_path)[0]

        if results.boxes is None or len(results.boxes) == 0:
            return {"disease": "Unknown", "confidence": 0.0, "bbox": None}

        box = max(results.boxes, key=lambda b: float(b.conf))
        cls_id     = int(box.cls)
        confidence = round(float(box.conf), 4)
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        classes = ["Bacterial Leaf Blight", "Brown Spot", "Leaf Smut"]
        disease = classes[cls_id] if cls_id < len(classes) else "Unknown"

        return {
            "disease":    disease,
            "confidence": confidence,
            "bbox":       [round(x1), round(y1), round(x2 - x1), round(y2 - y1)]
        }

    def _get_best_model(self, cnn: dict, resnet: dict, yolo: dict) -> str:
        scores = {
            "cnn":    cnn["confidence"],
            "resnet": resnet["confidence"],
            "yolo":   yolo["confidence"]
        }
        return max(scores, key=scores.get)