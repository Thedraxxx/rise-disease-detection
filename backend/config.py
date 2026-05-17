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
        "Leaf Blast": {
            "description": "Leaf blast is caused by the fungus Magnaporthe oryzae. It appears as diamond-shaped lesions with gray centers and brown borders.",
            "treatment": "Apply fungicides like Tricyclazole. Ensure proper field drainage and avoid excessive nitrogen fertilizer."
        },
        "Brown Spot": {
            "description": "Brown spot is caused by Bipolaris oryzae. It appears as oval brown spots scattered across the leaf surface.",
            "treatment": "Use fungicides like Iprodione. Improve soil nutrition, especially potassium levels."
        },
        "Bacterial Blight": {
            "description": "Bacterial blight is caused by Xanthomonas oryzae. Leaves show water-soaked to yellowish stripes along margins.",
            "treatment": "Use copper-based bactericides. Plant resistant varieties and avoid flood irrigation."
        },
        "Tungro": {
            "description": "Tungro is a viral disease transmitted by green leafhoppers. Infected plants show yellow-orange discoloration.",
            "treatment": "Control leafhopper population with insecticides. Use resistant varieties and remove infected plants."
        },
        "Healthy": {
            "description": "No disease detected. The rice leaf appears healthy.",
            "treatment": "Continue standard crop management practices."
        }
    }