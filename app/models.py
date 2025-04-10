from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), default='user')
    def set_password(self, passw):
        self.password_hash = generate_password_hash(passw)
    def check_password(self, passw):
        return check_password_hash(self.password_hash, passw)
    def history_pertanyaan(self):
        return Pertanyaan.query.filter_by(username=self.username).all()


class Surah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_surah = db.Column(db.Integer)
    nama_surah = db.Column(db.String(15), index=True)
    id_ayat = db.Column(db.Integer)
    text_ayat = db.Column(db.Text)
    text_ayat_perkata = db.Column(db.Text)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_surah = db.Column(db.String(15), index=True)
    waktu = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Pesan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dari = db.Column(db.Text)
    isi = db.Column(db.Text)
    waktu = db.Column(db.DateTime, default=datetime.utcnow)

    
class Pertanyaan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text)
    username = db.Column(db.String(50), default="Guest")
    waktu = db.Column(db.DateTime, default=datetime.utcnow)
