from app.models import db
from app.models.basemodel import BaseModel

class Categoria(BaseModel):
    
    __tablename__= 'categorias'
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    productos = db.relationship('Producto', back_populates='categoria')

    def to_dict(self, incluye_categoria = True):
      data = super().to_dict()
      data.update(
        {
        'nombre':self.nombre,
        'descripcion':self.descripcion
        })
      if incluye_categoria:
        data.update({'productos':[producto.to_dict(incluye_categoria = False, incluye_movimientos = False, incluye_proveedor = False) for producto in self.productos]})
      return data