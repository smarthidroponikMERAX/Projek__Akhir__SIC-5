#"""............................................................................................................."""
#""" Kode by MERA X """

#"""============================ LIBRARY ===================================="""
import streamlit as st #Digunakan untuk membuat website
import pandas as pd # Digunakan untuk memanggil library pandas (pandas untuk mengolah tabel data)
from pymongo import MongoClient #Digunakan untuk memanggil library Mongo
from sklearn.preprocessing import LabelEncoder #digunakan untuk membuat endcoding
from sklearn.model_selection import train_test_split #diguakan memisahkan data train dan data test
from sklearn.linear_model import LogisticRegression #digunkan sebagai model MachineLearning
from sklearn.ensemble import RandomForestClassifier#digunan sebagai model Machine Learning
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score #untuk Metrix Maachine Learning

st.set_page_config(page_title='Smart Hidroponik',layout="wide", page_icon="🍀") 

# """
# Untuk memberi judul pada tab browser, layout wide artinya menampilkan secara penuh web, page icon digunakan untuk memberi gambar di tab browser

# Penjelasan :
# kami menemukan kode untuk menampilkan icon di symbl.cc
# """


def ambil_data():
    #"""============================= INISIALISASI DATA ==================================="""
    print("\n============ DATA ================\n")
    
    #Memanggil data dari Mongodb atau lebih tepatnya adalah mengkoneksikan ke Mongodb
    # """ 
    # Penjelasan :
    
    # Alasan kami memanggil atau mengkoneksikan Mongodb 
    # dikarenakan data sensor pH, suhu, tds atau nutrisi yang ada di File .ino dikirim ke Flask 
    # lalu dikirim ke Mongodb, agar data kami disimpan di database
    # """
    
    client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
    #client adalah variabel yang berfungsi untuk mengkoneksikan Mongodb ke program ini, dan MongoClient adalah class dari library pymongo
    database = client['Smart_Hidroponik'] #untuk memilih atau mengkoneksikan database yang sudah kami tambahkan
    koleksi = database['Sensor'] #untuk memilih atau mengkoneksikan koleksi atau collection yang sudah kami tambahkan 
    
    # """
    # Penjelasan :
    
    # Kami mendapatkan format link tersebut dari website Mongodb, 
    # kami mendapatkannya dari tombol connect yang terdapat di overview,
    # lalu kami menekan timbil drivers sehingga muncul format link:
    # mongodb+srv://<username>:<password>@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik
    # """
    
    data_mongo = list(koleksi.find({}, {'_id': 0, 'pH': 1, 'tds': 1, 'suhu': 1}).sort('waktu', -1))
    # .find digunakan untuk mengambil semua data, data yang tampil hanya pH, tds/nutrisi, dan suhu, .sort digunakan untuk mengurutkan waktu terakhir masuk
    # list untuk Membuat menjadi list
    data_frame = pd.Dataframe(data_list) #agar data terstruktur dan rapi maka memerlukan dataframe dari pandas
    
    
    if data_list: #Jika data_list tidak kosong maka if akan mengembalikan data pertama dari list
      return data_list[0],data_frame
    else: #Jika tidak ada data maka else tidak akan terjadi apa apa
      None
    
    # """
    # Penjelasan :
    
    # Kami tidak menampilkan atau mengambil _id tidak terlalu penting, sehiingga hanya perlu mengambil atau menampilkan pH, tds/nutrisi,suhu.
    # lalu kami juga harus mengurutkan data terakhir bukan data pertama, maka dari itu index nya -1
    # """

def web():
    #"""============================DESAIN WEB================="""
    
    desain_css = """
        <style>
        
body { # untuk setting dari halaman keseluruhan
margin: 0; # pembatas bagian luar 
padding: 0; #pembatas bagian dalam
font-family: sans-serif; #jenis font
background-color: #fff; # warna backgroud
}
.bagian-header { #membuat header
    background-image: url("https://github.com/smarthidroponikMERAX/Projek__Akhir__SIC-5/blob/main/foto/bgHidroponik.jpg?raw=true");
    border-radius: 10px 10px 0 0; #membuat border menjadi sedikit bulat, 10px atas kiri, 10px atas kanan, 0 bawah kanan dan kiri
    border-bottom: 2px solid #eb0e0e; #border bawah diberi garis 2px
    margin: 0;
    padding: 20px;
    background-position: center; #posisi di tengah
    background-repeat: no-repeat; #pencegah pengulangan gambar
    background-size: cover; #memenuhi area
    height: 18.75em; #ukuran
}

#logo {
    width: 20%;
    border-radius: 30px;
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
                blue 0%, green 50%, red 100%);
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

    sensor_data = ambil_data()
    if sensor_data:
        pH = sensor_data['pH']
        suhu_air = sensor_data['suhu']
        nutrisi = sensor_data['tds']

    else:
        st.write('Tidak ada data sensor yang tersedia saat ini.')

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
          <span class="value">{ph_value}</span>
          <span class="unit">pH</span>
        </div>
      </div>
      <div class="sensor">
        <img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_suhu_air.png?raw=true" alt="icon_suhu" id="icon_suhu" /> 
        <h2>Suhu Air</h2>
        <div class="bagian_suhu">
          <span class="value">{suhu_value}</span>
          <span class="unit">°C</span>
        </div>
      </div>
      <div class="sensor">
        <img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_tds.png?raw=true" alt="icon_nutrisi" id="icon_nutrisi" />
        <h2>Nutrisi</h2>
        <div class="bagian_nutrisi">
          <span class="value">{tds_value}</span>
          <span class="unit">ppm</span>
        </div>
      </div>
    </div>
    <h1 class="status-hidroponik">Status hidroponik</h1>
    </div>
<div class="ukuran">
        <h1 class="batas-text">Ukuran pH</h1>
        <input type="range" min="1" max="14" value="{ph_value}" class="slide-ph" id="myRange">
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
        <p>pH tanamanmu: <span id="demo">{ph_value}</span></p>
    </div>
    <div class="ukuran">
        <h1 class="batas-text">Ukuran Suhu</h1>
        <input type="range" min="1" max="45" value="{suhu_value}" class="slide-suhu" id="myRange">
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
        <p>Suhu tanamanmu: <span id="demo">{suhu_value}</span></p>
    </div>
        <div class="ukuran">
        <h1 class="batas-text">Ukuran Nutrisi</h1>
        <input type="range" min="1" max="5000" value="{tds_value}" class="slide-nutrisi" id="myRange">
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
        <p>NUtrisi di tanamanmu: <span id="demo">{tds_value}</span></p>
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

def Machine_learning():
    data_frame = ambil_data()
    
    independen_ph = data_frame[['suhu', 'tds']] #indedependen_pH adalah variabel yang berisi dataframe yang mengambil data suhu dan tds
    dependen_ph = data_frame[['pH']] #dependen_pH adalah variabel yang berisi dataframe yang mengambil data pH
    
    #memisahkan data untuk prediksi Nutrisi/tds
    independen_nutrisi = data_frame[['suhu', 'pH']] #indedependen_pH adalah variabel yang berisi dataframe yang mengambil data suhu dan pH
    dependen_nutrisi = data_frame[['tds']] #dependen_pH adalah variabel yang berisi dataframe yang mengambil data tds atau Nutrisi
    
    """
    Penjelasan: 
    
    Kami memisahkan data pH dan Nutrisi/TDS menjadi dua buah dataframe yang berbeda,
    karena kami menginginkan prediksi data pH dan nutrisi/TDS maka kami memisahkan independen dan dependen menjadi 2 bagian yaitu bagian pH dan tds
    untuk prediksi pH kami menggunakan suhu dan tds/nutrisi sebagai acuan atau indepneden data
    untuk prediksi tds/nutrisi kami menggunakan suhu dan pH sebagai acuan atau indepneden data
    """

    
    st.title("Smart Hidroponik - Prediksi Kesehatan Tanaman")

    # Display the data
    st.subheader("Data Sensor")
    st.write(data_rapi)

    # Clean the data
    st.subheader("Pengecekan Data")
    st.write("Deskripsi Data:")
    st.write(data_rapi.describe())


