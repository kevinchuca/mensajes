from bolprex_app import create_app
# Ya no necesitamos importar 'db' ni 'text' aquí

app = create_app()

if __name__ == "__main__":
    app.run()