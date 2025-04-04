from app import app, db
from app.models import Surah, History, Pesan

from flask import jsonify, request, render_template
from sqlalchemy.sql import text




# @app.route("/api/surah/<surah>")
# def surah(surah):
#     hasil = Surah.query.filter_by(nama_surah=surah)
#     newHasil = {}
#     newHasil['ayat'] = []
#     for isi in hasil:
#         # newHasil['id_ayat']['id'].append(isi.id_ayat)
#         newHasil['ayat'].append(isi.text_ayat)
#     newHasil["id_surah"] = hasil[0].id_surah
#     newHasil["nama_surah"] = hasil[0].nama_surah
#     return jsonify(newHasil)


@app.route("/api/nama-surah")
def nama_surah():
    surah = Surah.query.with_entities(Surah.nama_surah).group_by(Surah.nama_surah).order_by(Surah.id_surah).all()
    hasil = [isi.nama_surah for isi in surah]
    return jsonify({"data": hasil})


@app.route("/api/get-surah/<nama>")
def getSurah(nama):
    surah = Surah.query.filter_by(nama_surah=nama).all()
    try:
        idSurah = 0 if surah[0].id_surah < 5 else (surah[0].id_surah - 5)
    except:
        return jsonify({'pesan':'Error'})
        
    nama_surah = Surah.query.with_entities(Surah.nama_surah).group_by(Surah.nama_surah).order_by(Surah.id_surah).filter(Surah.id_surah > idSurah).limit(9).all()
    rekomendasi = [isi.nama_surah for isi in nama_surah]
    try:
        rekomendasi.remove(nama)
    except:
        pass

    hasil = {
        "nama_surah": nama.upper(),
        "id_surah":None,
        "ayat": {},
        "jumlah_ayat":0,
        "rekomendasi": rekomendasi
    }
    for isi in surah:
        if hasil['id_surah'] == None:
            hasil['id_surah'] = isi.id_surah
        hasil['ayat'][f"{isi.id_ayat}"] = isi.text_ayat
        hasil['jumlah_ayat'] += 1
    try:
        his_surah = History(nama_surah=nama)
        db.session.add(his_surah)
        db.session.commit()
        print(f"Add history: {nama}")
    except:
        print(f"Gagal menambahkan history: {nama}")
    return jsonify(hasil)


@app.route("/api/get-surah-perkata/<nama>")
def getSurahPerkata(nama):
    surah = Surah.query.filter_by(nama_surah=nama).all()
    try:
        idSurah = 0 if surah[0].id_surah < 5 else (surah[0].id_surah - 5)
    except:
        return jsonify({'pesan':'Error'})
        
    nama_surah = Surah.query.with_entities(Surah.nama_surah).group_by(Surah.nama_surah).order_by(Surah.id_surah).filter(Surah.id_surah > idSurah).limit(9).all()
    rekomendasi = [isi.nama_surah for isi in nama_surah]
    try:
        rekomendasi.remove(nama)
    except:
        pass

    hasil = {
        "nama_surah": nama.upper(),
        "id_surah":None,
        "ayat": {},
        "jumlah_ayat":0,
        "rekomendasi": rekomendasi
    }

    for isi in surah:
        if hasil['id_surah'] == None:
            hasil['id_surah'] = isi.id_surah
        hasil['ayat'][f"{isi.id_ayat}"] = isi.text_ayat_perkata + isi.text_ayat[-1]
        hasil['jumlah_ayat'] += 1
    # try:
    #     his_surah = History(nama_surah=nama)
    #     db.session.add(his_surah)
    #     db.session.commit()
    #     print(f"Add history: {nama}")
    # except:
    #     print(f"Gagal menambahkan history: {nama}")
    return jsonify(hasil)


@app.route("/api/cari-ayat/<kata>")
def cari(kata):
    ayat = Surah.query.with_entities(Surah.id_surah, Surah.nama_surah, Surah.id_ayat, Surah.text_ayat).filter(Surah.text_ayat.like(f'%{kata}%')).all()
    hasil = {
        "ayat":[],
        "jumlah":0,
        "nama_surah": kata
    }
    for isi in ayat:
        tmp = ""
        tmp += (str(isi.id_surah) + ":")
        tmp += (isi.nama_surah + ":")
        tmp += (str(isi.id_ayat) + ":\n")
        tmp += (isi.text_ayat)
        hasil['ayat'].append(tmp)
        hasil['jumlah'] += 1
    return jsonify(hasil)


def search_surah(query):
    with db.engine.connect() as connection:
        print("Connect")
        result = connection.execute(text('''
            SELECT id_surah, nama_surah, id_ayat, text_ayat
            FROM surah_fts 
            WHERE surah_fts MATCH :query
        '''), {'query': query})
        return result.fetchall()
    

@app.route("/api/cari/<kata>")
def mencari(kata):
    print(kata)
    results = search_surah(kata)
    hasil = {
        "ayat":[],
        "jumlah":0,
        "nama_surah": kata
    }
    for isi in results:
        tmp = ""
        tmp += str(isi[0]) + ":"
        tmp += str(isi[1]) + ":"
        tmp += str(isi[2]) + "\n"
        tmp += str(isi[3])
        hasil['ayat'].append(tmp)
        hasil['jumlah'] += 1
    
    
    # response = [{'id_surah': result['id_surah'], 'nama_surah': result['nama_surah'], 'text_ayat': result['text_ayat']} for result in results]
    return jsonify(hasil)




@app.route("/api/cari-ayat2/<kata>")
def cari2(kata):
    kata = kata.split(' ')
    if len(kata) == 1:
        ayat = Surah.query.with_entities(Surah.id_surah, Surah.nama_surah, Surah.id_ayat, Surah.text_ayat).filter(Surah.text_ayat.like(f'%{kata[0]}%')).all()
    elif len(kata) == 2:
        ayat = Surah.query.with_entities(Surah.id_surah, Surah.nama_surah, Surah.id_ayat, Surah.text_ayat).filter(Surah.text_ayat.like(f'%{kata[0]}%'), Surah.text_ayat.like(f'%{kata[1]}%')).all()
    elif len(kata) >= 3:
        ayat = Surah.query.with_entities(Surah.id_surah, Surah.nama_surah, Surah.id_ayat, Surah.text_ayat).filter(Surah.text_ayat.like(f'%{kata[0]}%'), Surah.text_ayat.like(f'%{kata[1]}%'), Surah.text_ayat.like(f'%{kata[2]}%')).all()
    hasil = {
        "ayat":[],
        "jumlah":0,
        "nama_surah":" ".join(kata)
    }
    for isi in ayat:
        tmp = ""
        tmp += (str(isi.id_surah) + ":")
        tmp += (isi.nama_surah + ":")
        tmp += (str(isi.id_ayat) + ":\n")
        tmp += (isi.text_ayat)
        hasil['ayat'].append(tmp)
        hasil['jumlah'] += 1
    return jsonify(hasil)


@app.route("/api/kritik-dan-saran", methods=["POST"])
def kritik_dan_saran():
    data = request.get_json()
    dari = data.get("dari")
    pesan = data.get("pesan")
    if not pesan:
        return jsonify({'error':'Kami mengharapkan kritikan dan saran yang membangun'})
    try:
        add_pesan = Pesan(dari=dari,isi=pesan)
        db.session.add(add_pesan)
        db.session.commit()
        print(f"Pesan: {pesan}\nDari: {dari}")
        return jsonify({"pesan":"Terima kasih atas kritikan dan sarannya"})
    except:
        return jsonify({'error':'Maaf, saat ini kami mengalami kegagalan saan menyimpan pesan anda'})


@app.route('/umpan-balik')
def umpanBalik():
    daftar_pesan = Pesan.query.all()
    daftar_pesan = daftar_pesan[::-1]
    pesan = {}
    for isi in daftar_pesan:
        pesan[isi.id] = {
            'dari': isi.dari,
            'pesan': isi.isi,
            'waktu': isi.waktu.strftime('%d-%m-%Y')
        }
    print(pesan)
    dikunjungi = History.query.all()
    return render_template('index.html', chart_data=pesan, dikunjungi=len(dikunjungi))