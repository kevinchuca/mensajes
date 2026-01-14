from bolprex_app import create_app, db
import os

app = create_app()

# ESTO SE EJECUTARÁ SIEMPRE QUE LA APP ARRANQUE EN RENDER
with app.app_context():
    print("Sincronizando base de datos...")
    # db.drop_all()  # Descomenta esta línea si no te importa borrar los datos actuales para arreglarlo rápido
    db.create_all()
    
    # Si quieres mantener los datos pero agregar la columna, usa este bloque:
    try:
        db.session.execute(db.text('ALTER TABLE shipment ADD COLUMN client_name VARCHAR(120)'))
        db.session.commit()
        print("Columna client_name añadida.")
    except Exception as e:
        print(f"La columna ya existe o hubo un detalle: {e}")
        db.session.rollback()

if __name__ == "__main__":
    app.run()