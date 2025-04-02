from app import db
from datetime import datetime

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

    

