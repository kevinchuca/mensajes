import os
from datetime import datetime
import pytz
import cloudinary
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from .models import Shipment
from . import db

# Configuración de Cloudinary con las variables de Render
cloudinary.config( 
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.environ.get('CLOUDINARY_API_KEY'), 
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

ship_bp = Blueprint("ship", __name__, url_prefix="/shipments")

@ship_bp.get("/<int:shipment_id>")
@login_required
def detail(shipment_id):
    s = Shipment.query.get_or_404(shipment_id)
    return render_template("shipment_detail.html", s=s)

@ship_bp.post("/<int:shipment_id>/upload")
@login_required
def upload_delivery_photo(shipment_id):
    s = Shipment.query.get_or_404(shipment_id)
    
    if "photo" not in request.files:
        flash("No se envió archivo.", "warning")
        return redirect(url_for("ship.detail", shipment_id=shipment_id))
    
    file = request.files["photo"]
    
    if file.filename == "":
        flash("Archivo vacío.", "warning")
        return redirect(url_for("ship.detail", shipment_id=shipment_id))

    try:
        # 1. Subida directa a Cloudinary
        upload_result = cloudinary.uploader.upload(
            file, 
            folder="bolprex_entregas",
            public_id=f"entrega_{s.tracking_code}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        )

        # 2. Guardar la URL permanente en el campo delivered_photo del modelo Shipment
        s.delivered_photo = upload_result['secure_url'] 
        s.status = "ENTREGADO"
        
        # 3. Configurar hora local de Bolivia
        tz = pytz.timezone('America/La_Paz')
        s.delivered_at = datetime.now(tz)
        
        db.session.commit()
        flash("Prueba de entrega guardada exitosamente en la nube.", "success")
        
    except Exception as e:
        print(f"Error Cloudinary: {e}")
        flash("Error al subir la imagen. Verifique la conexión.", "danger")

    return redirect(url_for("ship.detail", shipment_id=shipment_id))