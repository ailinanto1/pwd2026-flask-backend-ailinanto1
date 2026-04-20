from app.controllers.proveedor_controller import ProveedorController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

proveedores = Blueprint('proveedores', __name__, url_prefix='/proveedores')

@proveedores.route('/')
@jwt_required()
@rol_access(['admin', 'operador'])
def get_all():
    return ProveedorController.get_all()

@proveedores.route('/<int:id>')
@jwt_required()
@rol_access(['admin', 'operador'])
def show(id):
    return ProveedorController.show(id)

@proveedores.route("/", methods=['POST'])
@jwt_required()
@rol_access(['admin'])
def create():
    return ProveedorController.create(request.get_json())

@proveedores.route("/<int:id>", methods=['PUT'])
@jwt_required()
@rol_access(['admin'])
def update(id):
    return  ProveedorController.update(request=request.get_json(), id=id)

@proveedores.route("/<int:id>", methods=['DELETE'])
@jwt_required()
@rol_access(['admin'])
def destroy(id):
    return ProveedorController.destroy( id)