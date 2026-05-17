import os
import uuid
from PIL import Image
from config import Config

class ImageService:

    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        return (
            "." in filename and
            filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def save_temp_image(file) -> str:
        """Save uploaded image temporarily and return the file path."""
        ext = file.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        return file_path

    @staticmethod
    def preprocess_image(file_path: str) -> Image.Image:
        """Open, convert and resize image to what models expect."""
        image = Image.open(file_path).convert("RGB")
        image = image.resize(Config.IMAGE_SIZE)
        return image

    @staticmethod
    def delete_temp_image(file_path: str) -> None:
        """Delete temp image after prediction is done."""
        if os.path.exists(file_path):
            os.remove(file_path)