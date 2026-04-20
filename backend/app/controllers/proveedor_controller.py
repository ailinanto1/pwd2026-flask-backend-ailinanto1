from typing import Literal

from sqlalchemy.exc import IntegrityError
from app.models.proveedor import Proveedor
from app.models.producto import Producto
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class ProveedorController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        proveedores_list = db.session.execute(db.select(Proveedor).order_by(db.desc(Proveedor.id))).scalars().all()
        if len(proveedores_list) > 0:
            proveedores_to_dict = [proveedor.to_dict() for proveedor in proveedores_list ]
            return jsonify(proveedores_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor:
            return jsonify(proveedor.to_dict()), 200
        return jsonify({"message": 'proveedor no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request.get('nombre')
        contacto:str = request.get('contacto')
        telefono:str = request.get('telefono')
        email:str = request.get('email')
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if error is None:
            try:
                proveedor = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono, email=email)
                db.session.add(proveedor)
                db.session.commit()
                return jsonify({'message': "proveedor creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "proveedor ya registrado"}), 409
        return jsonify ({'message': error}), 422
        
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request.get('nombre')
        contacto:str = request.get('contacto')
        telefono:str = request.get('telefono')
        email:str = request.get('email')
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if error is None:
            proveedor = db.session.get(Proveedor, id)
            if proveedor:
                try:
                    proveedor.nombre = nombre
                    proveedor.contacto = contacto
                    proveedor.telefono = telefono
                    proveedor.email = email
                    db.session.commit()
                    return jsonify({'message':'proveedor modificado con exito'}), 200
                except IntegrityError:
                    error = 'alguno de los datos ya existe' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'proveedor no encontrado'
            
        return jsonify({'message':error}), 404
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        
        if proveedor is None:
            return jsonify({'message': 'proveedor no encontrado'}), 404
        
        producto_asociado = db.session.execute(
            db.select(Producto).filter_by(proveedor_id=id)
        ).scalar()
        
        if producto_asociado is not None:
            return jsonify({
                'message': 'No se puede eliminar el proveedor porque tiene productos asociados'
            }), 409
        
        try:
            db.session.delete(proveedor)
            db.session.commit()
            return jsonify({'message': 'el proveedor fue eliminado con exito'}), 200
        except Exception:
            db.session.rollback()
            return jsonify({'message': 'Error interno al intentar eliminar'}), 500