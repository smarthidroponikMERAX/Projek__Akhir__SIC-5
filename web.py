"""............................................................................................................."""
""" Kode by MERA X """

"""============================ LIBRARY ===================================="""
import streamlit as st #Digunakan untuk membuat website
import pandas as pd # Digunakan untuk memanggil library pandas (pandas untuk mengolah tabel data)
from pymongo import MongoClient #Digunakan untuk memanggil library Mongo
from sklearn.preprocessing import LabelEncoder #digunakan untuk membuat endcoding
import seaborn as sns #seaborn untuk membuat heatmap/grafik berwarna
import matplotlib.pyplot as plt #pylot menampilkan heatmap
from sklearn.model_selection import train_test_split #diguakan memisahkan data train dan data test
from sklearn.linear_model import LogisticRegression #digunkan sebagai model MachineLearning
from sklearn.ensemble import RandomForestClassifier#digunan sebagai model Machine Learning
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score #untuk Metrix Maachine Learning

st.set_page_config(page_title='Smart Hidroponik',layout="wide", page_icon="🍀") 
"""
Untuk memberi judul pada tab browser, layout wide artinya menampilkan secara penuh web, page icon digunakan untuk memberi gambar di tab browser

Penjelasan :
kami menemukan kode untuk menampilkan icon di symbl.cc
"""

def ambil_data():
    """============================= INISIALISASI DATA ==================================="""
    print("\n============ DATA ================\n")
    
    #Memanggil data dari Mongodb atau lebih tepatnya adalah mengkoneksikan ke Mongodb
    """ 
    Penjelasan :
    
    Alasan kami memanggil atau mengkoneksikan Mongodb 
    dikarenakan data sensor pH, suhu, tds atau nutrisi yang ada di File .ino dikirim ke Flask 
    lalu dikirim ke Mongodb, agar data kami disimpan di database
    """
    
    client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
    #client adalah variabel yang berfungsi untuk mengkoneksikan Mongodb ke program ini, dan MongoClient adalah class dari library pymongo
    database = client['Smart_Hidroponik'] #untuk memilih atau mengkoneksikan database yang sudah kami tambahkan
    koleksi = database['Sensor'] #untuk memilih atau mengkoneksikan koleksi atau collection yang sudah kami tambahkan 
    
    """
    Penjelasan :
    
    Kami mendapatkan format link tersebut dari website Mongodb, 
    kami mendapatkannya dari tombol connect yang terdapat di overview,
    lalu kami menekan timbil drivers sehingga muncul format link:
    mongodb+srv://<username>:<password>@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik
    """
    
    data_mongo = koleksi.find({}, {'_id': 0, 'pH': 1, 'tds': 1, 'suhu': 1}).sort('waktu', -1)
    # .find digunakan untuk mengambil semua data, data yang tampil hanya pH, tds/nutrisi, dan suhu, .sort digunakan untuk mengurutkan waktu terakhir masuk
    data_list = list(data_mongo) # Membuat menjadi list
    
    
    if data_list: #Jika data_list tidak kosong maka if akan mengembalikan data pertama dari list
      return data_list[0]
    else: #Jika tidak ada data maka else tidak akan terjadi apa apa
      None
    
    """
    Penjelasan :
    
    Kami tidak menampilkan atau mengambil _id tidak terlalu penting, sehiingga hanya perlu mengambil atau menampilkan pH, tds/nutrisi,suhu.
    lalu kami juga harus mengurutkan data terakhir bukan data pertama, maka dari itu index nya -1
    """

def web():
    desain_css = """
        <style>
        
body { # untuk setting dari halaman keseluruhan
margin: 0; # pembatas bagian luar 
padding: 0; #pembatas bagian dalam
font-family: sans-serif; #jenis font
background-color: #fff; # warna backgroud
}
.bagian-header {
    background-image: url("https://raw.githubusercontent.com/Yeahthu/tes-streamlit/main/bgHidroponik.jpg");
    border-radius: 10px 10px 0 0;
    border-bottom: 2px solid #eb0e0e;
    margin: 0;
    padding: 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover; 
    text-align: center;
    height: 18.75em;
}

    
        </style>
