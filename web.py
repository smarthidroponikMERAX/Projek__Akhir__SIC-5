#kode by MERA X

#"""============================ LIBRARY ===================================="""
import streamlit as st  # Digunakan untuk memanggil library streamlit untuk website
import pandas as pd  # Digunakan untuk memanggil library pandas (pandas untuk mengolah tabel data)
from pymongo import MongoClient  #Digunakan untuk memanggil library Mongo
from sklearn.preprocessing import LabelEncoder  #digunakan untuk membuat endcoding
from sklearn.model_selection import train_test_split  #diguakan memisahkan data train dan data test
from sklearn.linear_model import LogisticRegression #digunkan sebagai model MachineLearning
from sklearn.ensemble import RandomForestClassifier  #digunan sebagai model Machine Learning
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score  #untuk Metrix


st.set_page_config(page_title='Smart Hidroponik', layout="wide", page_icon="🍀")



#"""============================= INISIALISASI DATA ==================================="""

#Memanggil data dari Mongodb atau lebih tepatnya adalah mengkoneksikan ke Mongodb 
# Penjelasan :
#Alasan kami memanggil atau mengkoneksikan Mongodb 
#dikarenakan data sensor pH, suhu, tds atau nutrisi yang ada di File .ino dikirim ke Flask 
#lalu dikirim ke Mongodb, agar data kami disimpan di database


client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
#client adalah variabel yang berfungsi untuk mengkoneksikan Mongodb ke program ini, dan MongoClient adalah class dari library pymongo
database = client['Smart_Hidroponik'] #untuk memilih atau mengkoneksikan database yang sudah kami tambahkan
koleksi = database['Sensor'] #untuk memilih atau mengkoneksikan koleksi atau collection yang sudah kami tambahkan

# """
#     Penjelasan :
    
#     Kami mendapatkan format link tersebut dari website Mongodb, 
#     kami mendapatkannya dari tombol connect yang terdapat di overview,
#     lalu kami menekan timbil drivers sehingga muncul format link:
#     mongodb+srv://<username>:<password>@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik
#     """

data_mongo = list(koleksi.find({}, {'_id': 0, 'pH': 1, 'tds': 1, 'suhu': 1,'waktu':1}).sort('waktu', -1))
# .find digunakan untuk mengambil semua data, data yang tampil hanya pH, tds/nutrisi, dan suhu, .sort digunakan untuk mengurutkan waktu terakhir masuk
data_frame = pd.DataFrame(data_mongo)  # Membuat menjadi list

 # """
 #    Penjelasan :
    
 #    Kami tidak menampilkan atau mengambil _id tidak terlalu penting, sehiingga hanya perlu mengambil atau menampilkan pH, tds/nutrisi,suhu.
 #    lalu kami juga harus mengurutkan data terakhir bukan data pertama, maka dari itu index nya -1
 # """


#"""============================DESAIN WEB================="""
desain_css = """
<style>

body{ # untuk setting dari halaman keseluruhan
margin: 0; # pembatas bagian luar 
padding: 0; #pembatas bagian dalam
font-family: sans-serif; #jenis font
background-color: #fff; # warna backgroud
}
.bagian-header{ 
background-image: url("https://github.com/smarthidroponikMERAX/Projek__Akhir__SIC-5/blob/main/foto/bgHidroponik.jpg?raw=true");
border-radius: 10px 10px 0 0; 
border-bottom: 2px solid #eb0e0e; 
margin: 0;
padding: 3em;
background-position: center; 
background-repeat: no-repeat; 
background-size: cover; 
text-align:center;
height: 19em; 
}
#logo {
width: 20%;
border-radius: 30px;
align-item: center;
}
.bagian-utama {
margin: 8px;
padding: 10px;
display: flex;
flex-wrap: wrap;
justify-content: space-between;
gap: 20px;
}
.bagian-utama > .sensor {
flex: 1 1 30%; /* Atur lebar sensor dengan proporsi */
text-align: center;
box-sizing: border-box;
}
.judul-overview {
font-size: 24px;
font-weight: bold;
width: 100%;
text-align: center;
margin: 20px;
color: red;
}
.sensor h2 {
margin: 0px;
font-size: 24px;
font-weight: bold;
color: red;
text-align: center;
}
.sensor {
padding: 0px;
margin: 1px;
}
#icon_pH, #icon_suhu, #icon_nutrisi {
width: 25%;
}
.bagian_ph, .bagian_suhu, .bagian_nutrisi {
font-size: 24px;
font-weight: bold;
margin: 10px;
}
.unit {
font-size: 12px;
color: #eb0e0e;
vertical-align: middle;
}
.bagian-akhir {
margin: 50em;
padding: 15px;
height: 20%;
}

.status-hidroponik {
font-size: 24px;
font-weight: bold;
width: 100%;
text-align: center;
margin: 20px;
margin-top: 200px;
color: #2E8B57;
}

.batas-text {
font-family: 'Courier New', Courier, monospace;
font-size: 20px;
text-align: center;
margin: 0px;
color: orange;
}

.ukuran {
width: 100%;
border-radius: 20px;
border-top: 4px solid RGB(169, 169, 169);
border-bottom: 4px solid RGB(169, 169, 169);
margin-bottom:3em;
margin-left: 0em;
margin-right: 14em;
padding: 15px;
box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

.slide-ph, .slide-suhu, .slide-nutrisi {
-webkit-appearance: none;
width: 100%;
margin: 30px 0;
}
.slide-ph:focus, .slide-suhu:focus, .slide-nutrisi:focus {
outline: none;
}

.slide-ph::-webkit-slider-runnable-track, .slide-suhu::-webkit-slider-runnable-track, .slide-nutrisi::-webkit-slider-runnable-track {
width: 100%;
height: 8.4px;
cursor: pointer;
border-radius: 10px;
border: 0.2px solid #010101;
}
.slide-ph::-webkit-slider-runnable-track {
background: linear-gradient(to right, 
        red 0%, rgb(255, 149, 0) 20%, 
        rgb(36, 249, 3) 30%, rgb(2, 82, 2) 50%, 
        rgb(45, 1, 76) 80%, purple 100%);
}
.slide-suhu::-webkit-slider-runnable-track {
background: linear-gradient(to right, 
        rgb(0, 42, 255) 0%, rgb(52, 63, 217) 20%, 
        rgb(145, 184, 219) 30%, rgb(0, 246, 45) 50%, 
        rgb(255, 149, 0) 80%, red 100%);
}

.slide-nutrisi::-webkit-slider-runnable-track {
background: linear-gradient(to right, 
        blue 0%,blue 30%,  green 40% ,green 50%, red 100%);
}

.slide-ph::-webkit-slider-thumb, .slide-suhu::-webkit-slider-thumb, .slide-nutrisi::-webkit-slider-thumb {
-webkit-appearance: none;
height: 23px;
width: 23px;
border-radius: 50%;
background-color: transparent;
background-image: url("https://github.com/Yeahthu/tes-streamlit/blob/main/kursor_fixx.png?raw=true");
background-size: cover;
cursor: pointer;
box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
margin-top: -21px;
}

.label {
display: flex;
justify-content: space-between;
margin: 10px;
padding: 10px;
font-size: 14px;
}

.info {
width: 33.33%;
text-align: center;
}

@media (max-width: 768px) {
.bagian-header {
height: 200px;
}
.judul-overview {
font-size: 18px;
}
.sensor h2 {
font-size: 20px;
}
.bagian_ph, .bagian_suhu, .bagian_nutrisi {
font-size: 18px;
}
.status-hidroponik {
font-size: 18px;
}
.batas-text {
font-size: 16px;
}
}
.red{
color: red;}
.green{
color:green;}
</style>
"""


if data_frame is not None: #membagi 3 variabel jika data_frame tidak kosong
    pH = data_frame['pH'].iloc[0]
    suhu_air =data_frame['suhu'].iloc[0]
    nutrisi = data_frame['tds'].iloc[0]
else: #jika data kosong maka write tidak ada data sensor tersedia
    st.write('Tidak ada data sensor yang tersedia saat ini.')
    pH, suhu_air, nutrisi = 0, 0, 0

#kode html
html_content = f"""
<div id = "Tampilan">
<div class = "bagian-header">
<img src="https://raw.githubusercontent.com/Yeahthu/tes-streamlit/main/logo%20fixx1.png" alt="logo" id="logo">
</div>
<h1 class="judul-overview">Ringkasan Hidroponik</h1>
<div class="bagian-utama">
<div class="sensor">
<img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_pH_new.png?raw=true" alt="icon_pH" id="icon_pH" />
<h2>pH Air</h2>
<div class="bagian_ph">
    <span class="value"{ 'red' if pH < 6.5 or pH > 7.5 else 'green' }">{pH}</span>
    <span class="unit">pH</span>
</div>
</div>
<div class="sensor">
<img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_suhu_air.png?raw=true" alt="icon_suhu" id="icon_suhu" /> 
<h2>Suhu Air</h2>
<div class="bagian_suhu">
    <span class="value" { 'red' if suhu_air < 20 or suhu_air > 26 else 'green' }>{suhu_air}</span>
    <span class="unit">°C</span>
</div>
</div>
<div class="sensor">
<img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_tds.png?raw=true" alt="icon_nutrisi" id="icon_nutrisi" />
<h2>Nutrisi</h2>
<div class="bagian_nutrisi">
    <span class="value" { 'red' if nutrisi < 1050 or nutrisi > 1300 else 'green' }>{nutrisi}</span>
    <span class="unit">ppm</span>
</div>
</div>
</div>
<h1 class="status-hidroponik">Status hidroponik</h1>
</div>
<div class="ukuran">
<h1 class="batas-text">Ukuran pH</h1>
<input type="range" min="1" max="14" value="{pH}" class="slide-ph" id="myRange">
<div class="label">
    <div class="info">Kadar rendah</div>
    <div class="info">Kadar sesuai</div>
    <div class="info">Kadar tinggi</div>
</div>
<div class="label">
    <div class="info">[1-4]</div>
    <div class="info">[5-7]</div>
    <div class="info">[9-14]</div>
</div>
<p>pH tanamanmu: <span id="demo">{pH}</span></p>
</div>
<div class="ukuran">
<h1 class="batas-text">Ukuran Suhu</h1>
<input type="range" min="1" max="45" value="{suhu_air}" class="slide-suhu" id="myRange">
<div class="label">
    <div class="info">Kadar rendah</div>
    <div class="info">Kadar sesuai</div>
    <div class="info">Kadar tinggi</div>
</div>
<div class="label">
    <div class="info">[Kurang dari 18 C]</div>
    <div class="info">[18 - 25 C]</div>
    <div class="info">[Lebih dar 25 C]</div>
</div>
<p>Suhu tanamanmu: <span id="demo">{suhu_air}</span></p>
</div>
<div class="ukuran">
<h1 class="batas-text">Ukuran Nutrisi</h1>
<input type="range" min="1" max="5000" value="{nutrisi}" class="slide-nutrisi" id="myRange">
<div class="label">
    <div class="info">Kadar rendah</div>
    <div class="info">Kadar sesuai</div>
    <div class="info">Kadar tinggi</div>
</div>
<div class="label">
    <div class="info">[Kurang dari 1050 ppm]</div>
    <div class="info">[1050 - 1400 ppm]</div>
    <div class="info">[Lebih dari 1400 ppm]</div>
</div>
<p>Nutrisi di tanamanmu: <span id="demo">{nutrisi}</span></p>
</div>
<script>
function updatePhColor(value) {{
var phElement = document.getElementById('phValue');
if (value < 5 || value > 7) {{
phElement.style.color = 'red';
}} else {{
phElement.style.color = 'green';
}}
}}
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;
slider.oninput = function() {{
    output.innerHTML = this.value;
    var cursorImage = "url(https://github.com/Yeahthu/tes-streamlit/blob/main/kursor_fixx.png?raw=true)";
    slider.style.cursor = cursorImage;
}}

</script>

"""

st.markdown(desain_css, unsafe_allow_html=True)
st.markdown(html_content, unsafe_allow_html=True)



    #menampilkan grafik 
    st.title("Grafik pH, suhu, Nutrisi")

if 'waktu' in data_frame.columns:
    data_frame['waktu'] = pd.to_datetime(data_frame['waktu'], errors='coerce')
    data_frame = data_frame.dropna(subset=['waktu'])
    data_frame['waktu'] = data_frame['waktu'].dt.strftime('%d-%b')
    # menyesuaikan format yang ada di database 

            
    st.subheader("Grafik Sensor")
    st.write("pH Sensor:")
    st.line_chart(data_frame.set_index('waktu')['pH'])#grafik yang menyesuaikan tanggal dan bulan dari database

    st.write("Suhu Air:")
    st.line_chart(data_frame.set_index('waktu')['suhu'])

    st.write("Nutrisi (TDS):")
    st.line_chart(data_frame.set_index('waktu')['tds'])
else:
    st.write("Kolom 'waktu' tidak ditemukan dalam data_frame. Pastikan nama kolom sudah benar.")


st.subheader("Pilih Machine Learning Model")
model_option = st.selectbox("Select Model", ("Linear Regression", "Random Forest")) #pilihan modelling ai

if model_option:
   st.success(f"{model_option} selected!")
   
def categorize_ph(value): #memastikan atau membuat cek kesehatan tanaman lewat pH
    if value < 5:
        return 'tidak sehat'
    elif 5 <= value <= 7:
        return 'sehat'
    else:
        return 'tidak sehat'

def categorize_tds(value): #memastikan atau membuat cek kesehatan tanaman lewat pH
    if value < 1050:
        return 'tidak sehat'
    elif 1050 <= value <= 1400:
        return 'sehat'
    else:
        return 'tidak sehat'

data_frame['pH kategori'] = data_frame['pH'].apply(categorize_ph) #menambahkan data 
data_frame['TDS kategori'] = data_frame['tds'].apply(categorize_tds)

#membuat semua data menjadi angka
label_encoder = LabelEncoder()
data_frame['TDS kategori'] = label_encoder.fit_transform(data_frame['TDS kategori'])
data_frame['pH kategori'] = label_encoder.fit_transform(data_frame['pH kategori'])


#memisahkan data independen dan dependen
independen_ph = data_frame[['suhu', 'tds']]
dependen_ph = data_frame['pH kategori']
independen_nutrisi = data_frame[['suhu', 'pH']]
dependen_nutrisi = data_frame['TDS kategori']

#melatih machine learning 
independen_train_ph, independen_test_ph, dependen_train_ph, dependen_test_ph = train_test_split(independen_ph, dependen_ph, test_size=0.25, stratify=dependen_ph)
independen_train_nutrisi, independen_test_nutrisi, dependen_train_nutrisi, dependen_test_nutrisi = train_test_split(independen_nutrisi, dependen_nutrisi, test_size=0.25, stratify=dependen_nutrisi)

#menggunakan model logistik regression
model_ph = LogisticRegression(class_weight='balanced') if model_option == "Linear Regression" else RandomForestClassifier(class_weight='balanced')
model_nutrisi = LogisticRegression(class_weight='balanced') if model_option == "Linear Regression" else RandomForestClassifier(class_weight='balanced')

#menambah keakuratan
model_ph.fit(independen_train_ph, dependen_train_ph)
hasil_prediksi_ph = model_ph.predict(independen_test_ph)

model_nutrisi.fit(independen_train_nutrisi, dependen_train_nutrisi)
hasil_prediksi_nutrisi = model_nutrisi.predict(independen_test_nutrisi)

#matrix machine learning
accuracy_ph = accuracy_score(dependen_test_ph, hasil_prediksi_ph)
precision_ph = precision_score(dependen_test_ph, hasil_prediksi_ph, average='macro')
recall_ph = recall_score(dependen_test_ph, hasil_prediksi_ph, average='macro')
f1_ph = f1_score(dependen_test_ph, hasil_prediksi_ph, average='macro')

accuracy_nutrisi = accuracy_score(dependen_test_nutrisi, hasil_prediksi_nutrisi)
precision_nutrisi = precision_score(dependen_test_nutrisi, hasil_prediksi_nutrisi, average='macro')
recall_nutrisi = recall_score(dependen_test_nutrisi, hasil_prediksi_nutrisi, average='macro')
f1_nutrisi = f1_score(dependen_test_nutrisi, hasil_prediksi_nutrisi, average='macro')


st.subheader("Evaluasi Model, ")
st.write(f"Accuracy (pH): {accuracy_ph:.2f}")
st.write(f"Precision (pH): {precision_ph:.2f}")
st.write(f"Recall (pH): {recall_ph:.2f}")
st.write(f"F1 Score (pH): {f1_ph:.2f}")

st.write(f"Accuracy (Nutrisi): {accuracy_nutrisi:.2f}")
st.write(f"Precision (Nutrisi): {precision_nutrisi:.2f}")
st.write(f"Recall (Nutrisi): {recall_nutrisi:.2f}")
st.write(f"F1 Score (Nutrisi): {f1_nutrisi:.2f}")


