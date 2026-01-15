from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Shipment, User, CITIES
from . import db

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def home():
    return render_template("home.html")

@main_bp.get("/dashboard")
@login_required
def dashboard():
    query = Shipment.query.order_by(Shipment.created_at.desc())
    numero_guia = request.args.get("numero_guia", "").strip()
    if numero_guia:
        query = query.filter(Shipment.numero_guia == numero_guia)
    
    if current_user.role == "admin":
        shipments = query.all()
    elif current_user.role == "mensajero":
        shipments = query.filter_by(messenger_id=current_user.id).all()
    else:
        shipments = query.filter_by(client_id=current_user.id).all()
    
    return render_template("dashboard.html", shipments=shipments)

@main_bp.get("/shipments/new")
@login_required
def new_shipment():
    if current_user.role not in ("admin", "mensajero"):
        flash("No autorizado.", "warning")
        return redirect(url_for("main.dashboard"))
    clients = User.query.filter_by(role="cliente").all()
    messengers = User.query.filter_by(role="mensajero").all()
    return render_template("new_shipment.html", cities=CITIES, clients=clients, messengers=messengers)

@main_bp.post("/shipments/create")
@login_required
def create_shipment():
    if current_user.role not in ("admin", "mensajero"):
        flash("No autorizado.", "warning")
        return redirect(url_for("main.dashboard"))

    from .utils import generate_tracking_code
    tracking_code = generate_tracking_code()

    ng = request.form.get("numero_guia", "").strip()
    if not ng:
        flash("El número de guía es obligatorio.", "danger")
        return redirect(url_for("main.new_shipment"))
    
    if Shipment.query.filter_by(numero_guia=ng).first():
        flash("El número de guía ya existe.", "danger")
        return redirect(url_for("main.new_shipment"))

    s = Shipment(
        tracking_code=tracking_code,
        numero_guia=ng,
        sender_name=request.form.get("sender_name"),
        recipient_name=request.form.get("recipient_name"),
        origin_city=request.form.get("origin_city"),
        destination_city=request.form.get("destination_city"),
        address=request.form.get("address"),
        status="PENDIENTE",
        notes=request.form.get("notes"),
        client_id=int(request.form.get("client_id")) if request.form.get("client_id") else None,
        messenger_id=int(request.form.get("messenger_id")) if request.form.get("messenger_id") else None,
    )
    db.session.add(s)
    db.session.commit()
    flash(f"Envío creado. Código: {tracking_code}", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/track", methods=["GET", "POST"])
def track():
    query = request.form.get("query") if request.method == "POST" else request.args.get("code", "").strip()
    shipment = None
    if query:
        from sqlalchemy import or_
        shipment = Shipment.query.filter(or_(Shipment.numero_guia == query.strip(), Shipment.tracking_code == query.strip())).first()
        if not shipment:
            flash("No se encontró el envío.", "warning")
    return render_template("track.html", shipment=shipment)

@main_bp.get("/shipments/<int:shipment_id>")
@login_required
def shipment_detail(shipment_id):
    s = Shipment.query.get_or_404(shipment_id)
    return render_template("shipment_detail.html", s=s)

@main_bp.post("/shipments/<int:shipment_id>/upload_photo")
@login_required
def upload_photo(shipment_id):
    from .utils import upload_image_to_cloudinary
    s = Shipment.query.get_or_404(shipment_id)
    
    file = request.files.get('file')
    if not file or file.filename == '':
        flash("No se seleccionó archivo.", "warning")
        return redirect(url_for("main.shipment_detail", shipment_id=shipment_id))

    try:
        image_url = upload_image_to_cloudinary(file)
        if image_url:
            s.photo_url = image_url
            s.status = "ENTREGADO"
            db.session.commit()
            flash("Entregado con éxito.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for("main.shipment_detail", shipment_id=shipment_id))

@main_bp.post("/shipments/<int:shipment_id>/delete")
@login_required
def delete_shipment(shipment_id):
    if current_user.role != "admin":
        flash("No autorizado.", "warning")
        return redirect(url_for("main.dashboard"))
    s = Shipment.query.get_or_404(shipment_id)
    db.session.delete(s)
    db.session.commit()
    flash("Envío eliminado.", "success")
    return redirect(url_for("main.dashboard"))