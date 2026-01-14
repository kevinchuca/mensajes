from bolprex_app import create_app, db # Asegúrate de importar 'db' también
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Estas dos líneas borran todo y crean la base de datos de nuevo
        db.drop_all() 
        db.create_all()
        print("Base de datos actualizada con éxito")
    app.run()