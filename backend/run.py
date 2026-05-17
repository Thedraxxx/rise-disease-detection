import os
from app import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    # Create uploads folder if it doesn't exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=True
    )