from flask import Flask, render_template
from config import Config

from routes.usuarios import usuarios_bp

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(usuarios_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/carrito")
def carrito():
    return render_template("carrito.html")

if __name__ == "__main__":
    app.run(debug=True)