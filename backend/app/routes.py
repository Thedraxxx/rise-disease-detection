from flask import Blueprint, request, current_app
from app.services.image_service import ImageService
from app.utils.response import success_response, error_response
from config import Config

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health_check():
    return success_response(data={"status": "running"}, message="Server is healthy")

@api.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return error_response("No image provided", 400)

    file = request.files["image"]

    if file.filename == "":
        return error_response("No image selected", 400)

    if not ImageService.is_allowed_file(file.filename):
        return error_response("File type not allowed. Use jpg, jpeg, png or webp", 400)

    temp_path = None

    try:
        # 4. Save image temporarily
        temp_path = ImageService.save_temp_image(file)

        # 5. Run all 3 models
        model_service = current_app.model_service
        results = model_service.predict_all(temp_path)

        # 6. Check if image is relevant
        if results.get("not_relevant"):
            return error_response("Image does not appear to be a rice leaf. Please upload a valid rice plant image.", 422)

        # 7. Get disease info for the winning model's disease
        best_disease = results[results["best_model"]]["disease"]
        disease_info = Config.DISEASE_INFO.get(best_disease, {})

        # 8. Build final response
        data = {
            "disease":     best_disease,
            "description": disease_info.get("description", ""),
            "treatment":   disease_info.get("treatment", ""),
            "best_model":  results["best_model"],
            "results": {
                "cnn":    results["cnn"],
                "resnet": results["resnet"],
                "yolo":   results["yolo"]
            }
        }

        return success_response(data=data, message="Prediction complete")

    except Exception as e:
        return error_response(f"Prediction failed: {str(e)}", 500)

    finally:
        if temp_path:
            ImageService.delete_temp_image(temp_path)