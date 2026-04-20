from app.controllers.producto_controller import ProductoController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

productos = Blueprint('productos', __name__, url_prefix='/productos')

@productos.route('/')
@jwt_required()
def get_all():
    return ProductoController.get_all()

@productos.route('/<int:id>')
@jwt_required()
def show(id):
    return ProductoController.show(id)

@productos.route("/", methods=['POST'])
@jwt_required()
@rol_access(['admin'])
def create():
    return ProductoController.create(request.get_json())

@productos.route("/<int:id>", methods=['PUT'])
@jwt_required()
@rol_access(['admin'])
def update(id):
    return  ProductoController.update(request=request.get_json(), id=id)

@productos.route("/<int:id>", methods=['DELETE'])
@jwt_required()
@rol_access(['admin'])
def destroy(id):
    return ProductoController.destroy( id)