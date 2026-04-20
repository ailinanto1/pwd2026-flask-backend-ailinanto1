from app.routes.auth_routes import auth_bp
from app.routes.rol_routes import roles
from app.routes.user_routes import users
from app.routes.producto_routes import productos
from app.routes.categoria_routes import categorias
from app.routes.movimientoStock_routes import movimientos
from app.routes.proveedor_routes import proveedores
from flask import Blueprint 

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api_v1')

api_v1.register_blueprint(users, url_prefix='/users')
api_v1.register_blueprint(roles, url_prefix='/roles')
api_v1.register_blueprint(auth_bp, url_prefix='/auth')
api_v1.register_blueprint(categorias, url_prefix='/categorias')
api_v1.register_blueprint(proveedores, url_prefix='/proveedores')
api_v1.register_blueprint(productos, url_prefix='/productos')
api_v1.register_blueprint(movimientos, url_prefix='/movimientos')