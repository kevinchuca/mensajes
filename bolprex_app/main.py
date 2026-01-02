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
    shipments = query.all()
    if current_user.role == "admin":
        shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    elif current_user.role == "mensajero":
        shipments = Shipment.query.filter_by(messenger_id=current_user.id).order_by(Shipment.created_at.desc()).all()
    else:
        shipments = Shipment.query.filter_by(client_id=current_user.id).order_by(Shipment.created_at.desc()).all()
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
    flash(f"Envío creado. Código de seguimiento: {tracking_code}", "success")
    return redirect(url_for("main.dashboard"))



@main_bp.get("/track")
@main_bp.post("/track")
def track():
    # allow searching by numero_guia or tracking_code via same input named 'query'
    query = request.form.get("query") if request.method == "POST" else request.args.get("code", "").strip()
    shipment = None
    if query:
        query = query.strip()
        from sqlalchemy import or_
        shipment = Shipment.query.filter(or_(Shipment.numero_guia == query, Shipment.tracking_code == query)).first()
        if not shipment:
            flash("No se encontró ningún envío con ese número de guía o código de rastreo.", "warning")
    return render_template("track.html", shipment=shipment)
@main_bp.get("/shipments/<int:shipment_id>/edit")
@login_required
def edit_shipment(shipment_id):
    if current_user.role != "admin":
        flash("Solo el administrador puede editar envíos.", "warning")
        return redirect(url_for("main.dashboard"))
    s = Shipment.query.get_or_404(shipment_id)
    return render_template("edit_shipment.html", s=s)

@main_bp.post("/shipments/<int:shipment_id>/update")
@login_required
def update_shipment(shipment_id):
    if current_user.role != "admin":
        flash("Solo el administrador puede editar envíos.", "warning")
        return redirect(url_for("main.dashboard"))
    s = Shipment.query.get_or_404(shipment_id)
    ng = request.form.get("numero_guia", "").strip()
    if not ng:
        flash("El número de guía es obligatorio.", "danger")
        return redirect(url_for("main.edit_shipment", shipment_id=shipment_id))
    if Shipment.query.filter(Shipment.numero_guia == ng, Shipment.id != shipment_id).first():
        flash("El número de guía ya existe.", "danger")
        return redirect(url_for("main.edit_shipment", shipment_id=shipment_id))
    s.numero_guia = ng
    s.sender_name = request.form.get("sender_name")
    s.recipient_name = request.form.get("recipient_name")
    s.origin_city = request.form.get("origin_city")
    s.destination_city = request.form.get("destination_city")
    s.address = request.form.get("address")
    s.notes = request.form.get("notes")
    db.session.commit()
    flash("Envío actualizado.", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.post("/shipments/<int:shipment_id>/delete")
@login_required
def delete_shipment(shipment_id):
    if current_user.role != "admin":
        flash("Solo el administrador puede eliminar envíos.", "warning")
        return redirect(url_for("main.dashboard"))
    s = Shipment.query.get_or_404(shipment_id)
    db.session.delete(s)
    db.session.commit()
    flash("Envío eliminado.", "success")
    return redirect(url_for("main.dashboard"))
