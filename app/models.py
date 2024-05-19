from app import db

class Surah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_surah = db.Column(db.Integer)
    nama_surah = db.Column(db.String(15), index=True)
    id_ayat = db.Column(db.Integer)
    text_ayat = db.Column(db.Text)
    text_ayat_perkata = db.Column(db.Text)
    

