from app.models.basemodel import BaseModel
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    
    __tablename__= 'users'
    nombre = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(200), unique =True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(255) )
    rol = db.relationship('Rol', back_populates='users')
    movimientos = db.relationship('MovimientoStock', back_populates='user')
    
    def to_dict(self, incluye_rol = True, incluye_movimientos = True):
      data = super().to_dict()
      data.update(
        {
        'nombre':self.nombre,
        'email':self.email

      })
      if incluye_rol:
        data['rol'] = self.rol.to_dict(incluye_user = False)
      if incluye_movimientos:
        data.update({'movimientos':[self.movimiento.to_dict(incluye_movimientos = False) for movimiento in self.movimientos]})
      return data
      
    def validate_password(self, password:str) -> bool:
      return check_password_hash(self.password, password)
    
    def generate_password(self, password:str):
      self.password = generate_password_hash(password)