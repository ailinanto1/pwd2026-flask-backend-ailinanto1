from app.controllers.movimientosStock_controller import MovimientoStockController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators.rol_access import rol_access


movimientos = Blueprint('movimientos', __name__, url_prefix='/movimientos')

@movimientos.route('/')
@jwt_required()
@rol_access(['admin', 'operador'])
def get_all():
    return MovimientoStockController.get_all()

@movimientos.route('/<int:id>')
@jwt_required()
@rol_access(['admin', 'operador'])
def show(id):
    return MovimientoStockController.show(id)

@movimientos.route("/mis")
@jwt_required()
def get_mis_movimientos():
    user_id = get_jwt_identity()
    return MovimientoStockController.get_mis_movimientos(user_id)

@movimientos.route("/", methods=['POST'])
@jwt_required()
def create():
    return MovimientoStockController.create(request.get_json())