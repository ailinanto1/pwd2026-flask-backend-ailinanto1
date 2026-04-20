from app.models.basemodel import BaseModel
from app.models import db

class Rol(BaseModel):
    __tablename__="roles"
    nombre = db.Column(db.String, unique = True)
    users = db.relationship('User', back_populates='rol')
        
    def to_dict(self, incluye_user = True):
        data = super().to_dict()
        data.update(
            {
            'nombre': self.nombre
        })
        if incluye_user:
            data.update({'users':[self.user.to_dict(incluye_user = False) for user in self.users]})
        return data
    