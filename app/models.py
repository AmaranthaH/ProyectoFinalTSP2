from . import db
from flask_login import UserMixin

class Persona(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    contrasena = db.Column(db.String(100))
    # Relación uno a muchos con ListaAnime
    animes = db.relationship('ListaAnime', backref='persona', lazy=True)


class PersonaSesion(db.Model):
    # Modelo para la segunda base de datos (SesionDatos.db)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    contrasena_hash = db.Column(db.String(255))
    salt = db.Column(db.String(255))

class ListaAnime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    capitulos = db.Column(db.String(100))
     # Claves foráneas
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    biblioteca_id = db.Column(db.Integer, db.ForeignKey('biblioteca_general_anime.id'), nullable=False)
    
class BibliotecaGeneralAnime(db.Model):
    # Modelo para la segunda base de datos (SesionDatos.db)
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    capitulos = db.Column(db.String(100))

