
# # ''' SMART HIDROPONIK || MERA X'''

# """ ================================ LIBRARY ================================="""
# from flask import Flask, request, jsonify # Memanggil flask untuk membuat local server, request untuk dan jsonify
# from pymongo import MongoClient as mongo # Untuk mengakses database menggunakan mongo 
# from pymongo.errors import ConnectionFailure 
# from datetime import datetime as dt # Datetime berfungsi agar dapat menampilkan waktu


# web = Flask(__name__) # untuk inisialisasi flask 

# """ ============================ MONGO (DATABASE) ====================================="""
# # Koneksi ke MongoDB
# url_database = "mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik"
# client_database = mongo(url_database) #klien dari database yang sudah kami buat
# database = client_database.Smart_Hidroponik #daabase yang kami buat
# koleksi_database = database.Sensor #koleksi_database ini berguna untuk menyimpan data perbagian

# """=============================== MENDAPATKAN DATA  ================================="""


# @web.route('/dapat_data', methods=['POST'])
# def dapat_data():
#     data = request.get_json()
#     waktu = dt.now().strftime("%d-%m-%Y ----- %H:%M:%S")

#     data['waktu'] = waktu

#     ''' ======= DATA PH =========='''
#     if 'pH' and 'tds' and 'suhu' in data: 
#         data['pH'] = float(data['pH'])
#         data['tds'] = float(data['tds'])
#         data['suhu'] = float(data['suhu'])
#         data_ada = koleksi_database.find_one({'waktu': waktu})

#         if data_ada:
#             return jsonify({"Pemberitahuan": "Data telah tersedia"}), 200
#         else:
#             koleksi_database.insert_one(data)
#             return jsonify({"Pemberitahuan": "Data berhasil disisipkan"}), 201
        
#     else:
#         return jsonify({"error": "Tidak ada data, mohon cek kembali"}), 400


# ''' ======= KONVERSI OBJECT_ID =========='''

# '''
#    Karena data _id memiliki tipe data object id dan 
#    JSON tak bisa membaca nya maka akan diubah ke string agar JSON dapat membaca
   
# '''
# def konversi_objectid(data): #method ini digunakan untuk mengkonversi object id
#     if isinstance(data, list): #isinstance ini mengecek apakah data adalah list 
#         for item in data: #perulangan digunakan untuk mengkonversi tiap data yang muncul
#             if '_id' in item: #mengecek _id ada di data 
#                 item['_id'] = str(item['_id']) # mengubahtipe data _id menjadi str
#     elif isinstance(data, dict): #isinstance ini mengecek apakah data adalah dictionary
#         '''
#         alasan tidak menggunakan perulangan karena list terdiri dari berbagai dictionary sehingga jika memastikan 
#         dictionary tidak memerlukan perulangan
#         '''
#         if '_id' in data: #mengecek _id ada di data 
#             data['_id'] = str(data['_id']) # mengubahtipe data _id menjadi str

#     return data #mengembalikan data

# @web.route('/data_sensor', methods=['GET'])
# def get_data():
#     data = list(koleksi_database.find())  # Fetch data from MongoDB
#     data = konversi_objectid(data)  # Convert ObjectId to string

#     return jsonify(data), 200

# if __name__ == '__main__':
#      web.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os

web = Flask(__name__)

# Koneksi ke MongoDB
url_database = "mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik"
mongo_uri = os.getenv('MONGO_URI',url_database)
client_database = MongoClient(mongo_uri)
database = client_database.Smart_Hidroponik
koleksi_database = database.Sensor

@web.route('/dapat_data', methods=['POST'])
def dapat_data():
    data = request.get_json()
    waktu = datetime.now().strftime("%d-%m-%Y ----- %H:%M:%S")
    data['waktu'] = waktu

    if 'pH' in data and 'tds' in data and 'suhu' in data:
        try:
            data['pH'] = round(float(data['pH']), 2)
            data['tds'] = round(float(data['tds']), 2)
            data['suhu'] = round(float(data['suhu']), 2)

            data_ada = koleksi_database.find_one({'waktu': waktu})
            if data_ada:
                return jsonify({"Pemberitahuan": "Data telah tersedia"}), 200
            else:
                koleksi_database.insert_one(data)
                return jsonify({"Pemberitahuan": "Data berhasil disisipkan"}), 201
        except ValueError as e:
            return jsonify({"error": "Format data tidak valid"}), 400
    else:
        return jsonify({"error": "Tidak ada data, mohon cek kembali"}), 400

def konversi_objectid(data):
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    elif isinstance(data, dict):
        if '_id' in data:
            data['_id'] = str(data['_id'])
    return data

@web.route('/data_sensor', methods=['GET'])
def get_data():
    data = list(koleksi_database.find())
    data = konversi_objectid(data) 
    # Menambahkan satuan ke data yang dikembalikan
    for item in data:
        if 'pH' in item and isinstance(item['pH'], (float, int)):
            item['pH'] = f"{item['pH']:.2f} pH"
        if 'tds' in item and isinstance(item['tds'], (float, int)):
            item['tds'] = f"{item['tds']:.2f} ppm"
        if 'suhu' in item and isinstance(item['suhu'], (float, int)):
            item['suhu'] = f"{item['suhu']:.2f} C"
    
    return jsonify(data), 200
@web.route('/data_sensor/delete/<string:date>', methods=['DELETE'])
def delete_data(date):
    try:
        # Konversi string tanggal ke format datetime
        date_obj = datetime.strptime(date, '%d-%m-%Y')

        # Menentukan rentang waktu untuk pencarian data
        start_date = date_obj.replace(hour=0, minute=0, second=0)
        end_date = date_obj.replace(hour=23, minute=59, second=59)

        # Melakukan penghapusan data berdasarkan rentang waktu
        result = koleksi_database.delete_many({'waktu': {'$gte': start_date, '$lte': end_date}})
        
        if result.deleted_count > 0:
            return jsonify({"message": f"Data dari tanggal {date} berhasil dihapus"}), 200
        else:
            return jsonify({"message": f"Tidak ada data dari tanggal {date}"}), 404
    except ValueError:
        return jsonify({"error": "Format tanggal tidak valid. Gunakan format dd-mm-yyyy"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    web.run(host='0.0.0.0', port=5000, debug=True)
