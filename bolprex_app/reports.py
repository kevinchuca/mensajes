from flask import Blueprint, send_file, request, current_app
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Shipment
from datetime import datetime

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

@reports_bp.get("/shipments/pdf")
def shipments_pdf():
    start = request.args.get("start")
    end = request.args.get("end")
    q = Shipment.query
    if start:
        q = q.filter(Shipment.created_at >= datetime.fromisoformat(start))
    if end:
        q = q.filter(Shipment.created_at <= datetime.fromisoformat(end))
    shipments = q.order_by(Shipment.created_at.desc()).all()

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Reporte de Envíos - BOLPREX")
    c.setFont("Helvetica", 10)
    y -= 30
    for s in shipments:
        line = f"{s.tracking_code} | {s.sender_name} -> {s.recipient_name} | {s.destination_city} | {s.status} | {s.created_at.strftime('%Y-%m-%d')}"
        c.drawString(50, y, line[:120])
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 50
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_envios.pdf", mimetype="application/pdf")
