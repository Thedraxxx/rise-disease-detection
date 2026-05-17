from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.services.model_service import ModelService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.model_service = ModelService()

    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    # ── Error handlers ────────────────────────────────────────────────────────

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "status": "error",
            "message": "Bad request. Please check your input.",
            "data": None
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found.",
            "data": None
        }), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({
            "status": "error",
            "message": "Image too large. Max size is 10MB.",
            "data": None
        }), 413

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({
            "status": "error",
            "message": "Could not process the image.",
            "data": None
        }), 422

    @app.errorhandler(429)
    def too_many_requests(e):
        return jsonify({
            "status": "error",
            "message": "Too many requests. Please wait a moment.",
            "data": None
        }), 429

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "status": "error",
            "message": "Server error. Something went wrong on our end.",
            "data": None
        }), 500

    @app.errorhandler(503)
    def service_unavailable(e):
        return jsonify({
            "status": "error",
            "message": "Server is unavailable. Please try again later.",
            "data": None
        }), 503

    return app