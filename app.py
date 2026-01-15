from bolprex_app import create_app, db
from sqlalchemy import text

app = create_app()

# Este bloque se ejecutará al iniciar en Render
with app.app_context():
    try:
        # Intentamos añadir la columna faltante directamente
        db.session.execute(text('ALTER TABLE shipment ADD COLUMN client_name VARCHAR(120)'))
        db.session.commit()
        print("Columna client_name añadida con éxito.")
    except Exception as e:
        # Si la columna ya existe, simplemente ignoramos el error
        db.session.rollback()
        print(f"Aviso: {e}")

if __name__ == "__main__":
    app.run()