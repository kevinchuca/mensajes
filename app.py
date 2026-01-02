from flask import Flask




app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 BOLPREX SRL - Sistema Flask listo para Render"

if __name__ == "__main__":
    pass
