import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # Server
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 5000

    # Upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max image size

    # Model
    MODELS_FOLDER = os.path.join(BASE_DIR, "app", "models")
    IMAGE_SIZE = (128, 128)  # size models expect

    # Disease descriptions
    DISEASE_INFO = {
    "Brown Spot": {
        "description": "Brown spot is caused by the fungus Bipolaris oryzae. It appears as oval to circular brown spots scattered across the leaf surface, often with a yellow halo.",
        "treatment": "Use fungicides like Iprodione or Propiconazole. Improve soil nutrition especially potassium and silicon levels."
    },
    "Bacterial Leaf Blight": {
        "description": "Bacterial leaf blight is caused by Xanthomonas oryzae pv. oryzae. Leaves show water-soaked to yellowish stripes along margins that turn white or gray.",
        "treatment": "Use copper-based bactericides. Plant resistant varieties, avoid flood irrigation and excessive nitrogen."
    },
    "Leaf Smut": {
        "description": "Leaf smut is caused by the fungus Entyloma oryzae. It appears as small, angular, black spots scattered on both leaf surfaces.",
        "treatment": "Apply fungicides like Carbendazim. Use certified disease-free seeds and maintain field hygiene."
    },
    "Healthy": {
        "description": "No disease detected. The rice leaf appears healthy.",
        "treatment": "Continue standard crop management practices."
    }
}