from bolprex_app import create_app, db
from sqlalchemy import text

app = create_app()

# Este bloque se encarga de actualizar la base de datos en Render
with app.app_context():
    try:
        # Aseguramos que existan las columnas necesarias para las fotos
        db.session.execute(text('ALTER TABLE shipment ADD COLUMN IF NOT EXISTS photo_url VARCHAR(255)'))
        db.session.commit()
        print("Base de datos actualizada correctamente.")
    except Exception as e:
        db.session.rollback()
        print(f"Nota sobre la base de datos: {e}")

if __name__ == "__main__":
    app.run()