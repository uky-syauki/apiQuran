from app import app
from app.models import Surah

from flask import jsonify

@app.route("/api/surah/<surah>")
def surah(surah):
    hasil = Surah.query.filter_by(nama_surah=surah)
    newHasil = {}
    newHasil['ayat'] = []
    for isi in hasil:
        # newHasil['id_ayat']['id'].append(isi.id_ayat)
        newHasil['ayat'].append(isi.text_ayat)
    newHasil["id_surah"] = hasil[0].id_surah
    newHasil["nama_surah"] = hasil[0].nama_surah
    return jsonify(newHasil)