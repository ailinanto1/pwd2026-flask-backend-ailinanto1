from app.models.basemodel import BaseModel
from app.models import db

class MovimientoStock(BaseModel):
    
    __tablename__= 'movimientostock'
    tipo = db.Column(db.String(10))
    cantidad = db.Column(db.Integer, nullable = False)
    motivo = db.Column(db.String(200), nullable = True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    producto = db.relationship('Producto', back_populates='movimientos')
    user = db.relationship('User', back_populates='movimientos')
    
    def to_dict(self, incluye_producto  = True, incluye_user = True):
      data = super().to_dict()
      data.update(
        {
        'tipo':self.tipo,
        'cantidad':self.cantidad,
        'motivo':self.motivo,
        'producto_id':self.producto_id,
        'user_id':self.user_id,
      })
      if incluye_producto:
        data.update({'producto':self.producto.to_dict(incluye_proveedor = False, incluye_movimientos = False)})
      if incluye_user:
        data.update({'user': self.user.to_dict(incluye_movimientos=False)})
        return data