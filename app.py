from bolprex_app import create_app, db # Asegúrate de importar db
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # ESTO ES LO QUE SOLUCIONA EL ERROR:
        print("Borrando y recreando tablas...")
        db.drop_all() 
        db.create_all()
        print("Base de datos actualizada con la columna client_name")
    
    app.run()