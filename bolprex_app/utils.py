import cloudinary
import cloudinary.uploader
import os

# Esta configuración conecta tu código con las variables que mostraste en Render
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

def upload_image_to_cloudinary(file):
    try:
        # Subida directa a la nube
        upload_result = cloudinary.uploader.upload(
            file,
            folder="bolprex_entregas"
        )
        # Retorna la URL segura que guardaremos en photo_url
        return upload_result.get("secure_url")
    except Exception as e:
        # Esto permite ver el error exacto en los Logs de Render
        print(f"DEBUG - Error en Cloudinary: {str(e)}")
        return None