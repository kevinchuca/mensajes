from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

ROLES = ("admin", "mensajero", "cliente")
CITIES = ("La Paz", "Santa Cruz", "Cochabamba", "Tarija", "Oruro", "Potosí", "Trinidad", "Sucre")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="cliente", nullable=False)
    city = db.Column(db.String(50))

    # Relaciones
    shipments_client = db.relationship("Shipment", backref="client", foreign_keys="Shipment.client_id", lazy=True)
    shipments_messenger = db.relationship("Shipment", backref="messenger", foreign_keys="Shipment.messenger_id", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(20), unique=True, nullable=False)
    numero_guia = db.Column(db.String(50), unique=True, nullable=False)
    sender_name = db.Column(db.String(120), nullable=False)
    recipient_name = db.Column(db.String(120), nullable=False)
    origin_city = db.Column(db.String(50), nullable=False)
    destination_city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="PENDIENTE", nullable=False)
    notes = db.Column(db.String(300))
    
    # Campo para clientes sin cuenta (Simplificado)
    client_name = db.Column(db.String(120)) 

    # Campos para la entrega (Cloudinary y Fecha)
    delivered_photo = db.Column(db.String(300))
    delivered_at = db.Column(db.DateTime)

    # Relaciones con usuarios existentes
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    messenger_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)