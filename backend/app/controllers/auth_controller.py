from app.models import db
from app.models.user import User
from app.models.rol import Rol
from flask import Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

class AuthController:
    @staticmethod
    def Register(request:dict) -> tuple[Response, int]:
        nombre:str | None = request.get('nombre')
        email:str | None = request.get('email')
        password:str | None = request.get('password')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if email is None:
            error = 'El email es requerido'
        if password is None:
            error = 'La contraseña es requerida'
            
        if error is None:
            try:
                rol_operador = db.session.execute(db.select(Rol).filter_by(nombre='operador')).scalar_one_or_none()
                if rol_operador and nombre and password and email is not None:
                    user = User(nombre=nombre, email=email, rol_id=rol_operador.id, password=password)    
                    user.generate_password(password)
                    db.session.add(user)
                    db.session.commit()
                return jsonify({'message': "usuario creado con exito"}), 201               
                
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "Usuario ya registrado"}), 409
        return jsonify ({'message': error}), 422
    
    @staticmethod
    def login(request : dict  ) -> tuple[Response, int]:
        
        nombre:str|None = request.get('nombre')
        password:str | None = request.get('password')
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if password is None:
            error = 'La contraseña es requerida'
            
        if error is None:
            user = db.session.execute(db.select(User).filter_by(nombre=nombre)).scalar_one_or_none()
            if user and user.validate_password(password):
                rol_nombre = user.rol.nombre if user.rol else None
                access_token = create_access_token(identity=str(user.id), additional_claims={'rol': user.rol.nombre if user.rol else None})
                return jsonify({'access_token': access_token, 'rol': rol_nombre if user.rol else None, 'nombre': user.nombre}), 200
            return jsonify({'message': "Credenciales inválidas"}), 401
        return jsonify ({'message': error}), 422

    @staticmethod
    def me() -> tuple[Response, int]:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"message": "Usuario no encontrado"}), 404