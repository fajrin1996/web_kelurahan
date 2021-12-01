from sqlalchemy.orm import backref
from affairs import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def load_user(admindb_id):
    return admindb.query.get(int(admindb_id))

class admindb(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"admindb('{self.username}','{self.email}','{self.password}')"

class Kategori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    artikel_id = db.relationship('Artikel', backref='ar', lazy=True)

    def __repr__(self):
        return f"Kategori('{self.nama}')"
         
class Artikel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    konten = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(255), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=False)

    def __repr__(self):
        return f"Artikel('{self.judul}','{self.konten}','{self.thumbnail}','{self.tgl_post}')"

class JsonEncodeDict(db.TypeDecorator):
  impl = db.Text

  def process_bind_param(self, value, dialect):
    if value is None:
      return '{}'
    else:
      return json.dumps(value)
  def process_result_value(self, value, dialect):
    if value is None:
      return {}
    else:
      return json.loads(value)

class CustomerPgAir(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  tgl_pst = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  csv_field = db.Column(JsonEncodeDict)

  def __repr__(self):
    return f"CustomerPgAir('{self.tgl_pst}','{self.csv_field}')"
  

# db.create_all()