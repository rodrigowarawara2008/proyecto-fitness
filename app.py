from flask import Flask, redirect
from config import Config

from routes.usuarios import usuarios_bp
from routes.productos import productos_bp
from routes.carrito import carrito_bp

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(carrito_bp)

# Al entrar a la web va directo a la tienda
@app.route('/')
def index():
    return redirect('/inicio')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)