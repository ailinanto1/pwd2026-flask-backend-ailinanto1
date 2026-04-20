from app.models.basemodel import BaseModel
from app.models import db

class Proveedor(BaseModel):
    
    __tablename__= 'proveedores'
    nombre = db.Column(db.String(150), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120))
    productos = db.relationship('Producto', back_populates='proveedor')

    def to_dict(self, incluye_proveedor = True):
      data = super().to_dict()
      data.update(
        {
        'nombre':self.nombre,
        'contacto':self.contacto,
        'telefono':self.telefono,
        'email':self.email
      })
      if incluye_proveedor:
        data.update({'productos':[producto.to_dict(incluye_proveedor=False,incluye_movimientos=False) for producto in self.productos]})      
      return data