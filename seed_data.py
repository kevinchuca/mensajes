from bolprex_app import create_app, db
from bolprex_app.models import User, Shipment
from datetime import datetime

app = create_app()
with app.app_context():
    # Create client user
    if not User.query.filter_by(email="cliente@bolprex.com").first():
        u = User(name="Cliente Prueba", email="cliente@bolprex.com", role="cliente")
        u.set_password("cliente123")
        db.session.add(u)
        db.session.commit()
        print("Usuario cliente creado: cliente@bolprex.com / cliente123")
    else:
        print("Usuario cliente ya existe.")

    # Create a sample shipment
    if not Shipment.query.filter_by(numero_guia="GUIA98765").first():
        client = User.query.filter_by(email="cliente@bolprex.com").first()
        s = Shipment(
            tracking_code="TRACK12345",
            numero_guia="GUIA98765",
            sender_name="Empresa Ejemplo",
            recipient_name="Juan Pérez",
            origin_city="La Paz",
            destination_city="Cochabamba",
            address="Av. América #123",
            status="En tránsito",
            client_id=client.id if client else None,
            created_at=datetime.utcnow()
        )
        db.session.add(s)
        db.session.commit()
        print("Envío de prueba creado: GUIA98765 / TRACK12345")
    else:
        print("Envío de prueba ya existe.")
