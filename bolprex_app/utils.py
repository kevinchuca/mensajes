import cloudinary
import cloudinary.uploader

def upload_image_to_cloudinary(file):
    try:
        # Forzamos la subida a Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Error en Cloudinary: {e}")
        return None