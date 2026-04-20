from typing import Literal

from sqlalchemy.exc import IntegrityError
from app.models.producto import Producto
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller
from datetime import datetime

class ProductoController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        productos_list = db.session.execute(db.select(Producto).order_by(db.desc(Producto.id))).scalars().all()
        if len(productos_list) > 0:
            Productos_to_dict = [Producto.to_dict() for Producto in productos_list ]
            return jsonify(Productos_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if Producto:
            return jsonify(producto.to_dict()), 200
        return jsonify({"message": 'producto no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request.get('nombre')
        descripcion:str = request.get('descripcion')
        precio_costo:int = request.get('precio_costo')
        precio_venta:int = request.get('precio_venta')
        stock_actual:int = request.get('stock_actual')
        stock_minimo:int = request.get('stock_minimo')
        categoria_id:int = request.get('categoria_id')
        proveedor_id:int = request.get('proveedor_id')
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if precio_costo is None:
            error = 'El precio es requerido'
        if precio_venta is None:
            error = 'El precio es requerido'
        if stock_actual is None:
            error = 'El stock es requerido'
        if stock_minimo is None:
            error = 'El stock es requerido'
        if categoria_id is None:
            error = 'La categoria es requerida'
        
        from app.models.categoria import Categoria
        cat = db.session.get(Categoria, categoria_id)
        if not cat:
            error = 'La categoría no existe, no podés crear el producto'
        if error is None:
            try:
                producto = Producto(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio_costo=precio_costo,
                    precio_venta=precio_venta,
                    stock_actual=stock_actual,
                    stock_minimo=stock_minimo,
                    categoria_id=categoria_id,
                    proveedor_id=proveedor_id)
                db.session.add(producto)
                db.session.commit()
                return jsonify({'message': "producto creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "producto ya registrado"}), 409
        return jsonify ({'message': error}), 422
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request.get('nombre')
        descripcion:str = request.get('descripcion')
        precio_costo:int = request.get('precio_costo')
        precio_venta:int = request.get('precio_venta')
        stock_actual:int = request.get('stock_actual')
        stock_minimo:int = request.get('stock_minimo')
        categoria_id:int = request.get('categoria_id')
        proveedor_id:int = request.get('proveedor_id')
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if precio_costo is None:
            error = 'El precio es requerido'
        if precio_venta is None:
            error = 'El precio es requerido'
        if stock_actual is None:
            error = 'El stock es requerido'
        if stock_minimo is None:
            error = 'El stock es requerido'
        if categoria_id is None:
            error = 'La categoria es requerida'
        if error is None:
            producto = db.session.get(Producto, id)
            if producto:
                try:
                    producto.nombre = nombre
                    producto.descripcion = descripcion
                    producto.precio_costo = precio_costo
                    producto.precio_venta = precio_venta
                    producto.stock_actual = stock_actual
                    producto.stock_minimo = stock_minimo
                    producto.categoria_id = categoria_id
                    producto.proveedor_id = proveedor_id
                    producto.updated_at = datetime.now()
                    db.session.commit()
                    return jsonify({'message':'producto modificado con exito'}), 200
                except IntegrityError:
                    error = 'alguno de los datos ya existe' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'producto no encontrado'
            
        return jsonify({'message':error}), 404
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        error = None
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'message':'el producto fue eliminado con exito'}), 200
        else:
            error = 'producto no encontrado'
        return jsonify({'message':error}), 404