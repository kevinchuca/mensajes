from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .models import User, Shipment
from . import db
from datetime import timedelta, datetime
from werkzeug.utils import secure_filename
import os

api_bp = Blueprint("api", __name__, url_prefix="/api")

def init_api(app):
    jwt = JWTManager(app)
    app.register_blueprint(api_bp)

@api_bp.post("/login")
def api_login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg":"Credenciales inválidas"}), 401
    access = create_access_token(identity={"id": user.id, "role": user.role}, expires_delta=timedelta(days=7))
    return jsonify(access_token=access)

@api_bp.route("/shipments/<int:shipment_id>/upload", methods=["POST"])
@jwt_required()
def api_upload(shipment_id):
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])
    if user.role != "mensajero" and user.role != "admin":
        return jsonify({"msg":"No autorizado"}), 403
    s = Shipment.query.get_or_404(shipment_id)
    if "photo" not in request.files:
        return jsonify({"msg":"No file"}), 400
    f = request.files["photo"]
    if f.filename == "":
        return jsonify({"msg":"Empty filename"}), 400
    if '.' in f.filename and f.filename.rsplit('.',1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'png','jpg','jpeg','gif'}):
        fn = secure_filename(f"{s.tracking_code}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{f.filename.rsplit('.',1)[1].lower()}")
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], fn)
        f.save(save_path)
        s.delivered_photo = f"uploads/{fn}"
        s.status = "ENTREGADO"
        s.delivered_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"msg":"Foto subida", "photo": s.delivered_photo})
    return jsonify({"msg":"Formato no permitido"}), 400
