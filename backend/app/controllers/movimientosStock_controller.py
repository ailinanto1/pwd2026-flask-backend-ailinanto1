from typing import Literal

from sqlalchemy.exc import IntegrityError
from app.models.movimientoStock import MovimientoStock
from app.models.producto import Producto
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class MovimientoStockController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientoStocks_list = db.session.execute(db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientoStocks_list) > 0:
            movimientoStocks_to_dict = [movimientoStock.to_dict() for movimientoStock in movimientoStocks_list ]
            return jsonify(movimientoStocks_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        movimientoStock = db.session.get(MovimientoStock, id)
        if MovimientoStock:
            return jsonify(movimientoStock.to_dict()), 200
        return jsonify({"message": 'tipo de movimiento no encontrado'}), 404
    
    @staticmethod
    def get_mis_movimientos(id)->tuple[Response, int]:
        movimientoStocks_list = db.session.execute(db.select(MovimientoStock).filter_by(user_id = id).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientoStocks_list) > 0:
            movimientoStocks_to_dict = [movimientoStock.to_dict() for movimientoStock in movimientoStocks_list ]
            return jsonify(movimientoStocks_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        tipo:str = request.get('tipo')
        cantidad:int = request.get('cantidad')
        motivo:int = request.get('motivo')
        producto_id:int = request.get('producto_id')
        user_id:int = request.get('user_id')
        error :str | None = None
        if tipo is None:
            error = 'El tipo es requerido'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if producto_id is None:
            error = 'El producto_id es requerido'
        if user_id is None:
            error = 'El user_id es requerido'
        producto = db.session.get(Producto, producto_id)
        if producto.stock_actual < cantidad and tipo == 'salida':
            error = 'No hay suficiente stock'
        
        if error is None:
            try:
                if tipo == 'salida':
                    producto.stock_actual = producto.stock_actual - cantidad
                else:
                    producto.stock_actual = producto.stock_actual + cantidad
                movimientoStock = MovimientoStock(
                    tipo=tipo,
                    cantidad=cantidad,
                    motivo=motivo,
                    producto_id=producto_id,
                    user_id=user_id)
                db.session.add(movimientoStock)
                db.session.commit()
                return jsonify({'message': "tipo de movimiento creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "tipo de movimiento ya registrado"}), 409
        return jsonify ({'message': error}), 422
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        tipo:str = request.get('tipo')
        cantidad:int = request.get('cantidad')
        motivo:int = request.get('motivo')
        producto_id:int = request.get('producto_id')
        user_id:int = request.get('user_id')
        error :str | None = None
        if tipo is None:
            error = 'El tipo es requerida'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if producto_id is None:
            error = 'El producto_id es requerido'
        if user_id is None:
            error = 'El user_id es requerido'
        if error is None:
            movimientoStock = db.session.get(MovimientoStock, id)
            if movimientoStock:
                try:
                    movimientoStock.tipo = tipo
                    movimientoStock.cantidad = cantidad
                    movimientoStock.motivo = motivo
                    movimientoStock.producto_id = producto_id
                    movimientoStock.user_id = user_id
                    db.session.commit()
                    return jsonify({'message':'tipo de movimiento modificado con exito'}), 200
                except IntegrityError:
                    error = 'algunos de los datos ya existe' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'tipo de movimiento no encontrado'
            
        return jsonify({'message':error}), 404
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        movimientoStock = db.session.get(MovimientoStock, id)
        error = None
        if movimientoStock:
            db.session.delete(movimientoStock)
            db.session.commit()
            return jsonify({'message':'tipo de movimiento fue eliminado con exito'}), 200
        else:
            error = 'tipo de movimiento no encontrado'
        return jsonify({'message':error}), 404