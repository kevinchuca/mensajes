import cloudinary
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ESTO ES LO QUE FALTA: Activa la conexión con tus llaves de Render
cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API_KEY'), 
    api_secret = os.getenv('CLOUDINARY_API_SECRET'),
    secure = True
)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    
    # Arreglo para la base de datos de Render (postgres:// -> postgresql://)
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{BASE_DIR / 'bolprex.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "static" / "uploads"))
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-key")