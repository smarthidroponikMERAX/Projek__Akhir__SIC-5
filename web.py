#"""============================ LIBRARY ===================================="""
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score



st.set_page_config(page_title='Smart Hidroponik', layout="wide", page_icon="🍀")



#"""============================= INISIALISASI DATA ==================================="""


client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
database = client['Smart_Hidroponik']
koleksi = database['Sensor']

data_mongo = list(koleksi.find({}, {'_id': 0, 'pH': 1, 'tds': 1, 'suhu': 1,'waktu':1}).sort('waktu', -1))
data_frame = pd.DataFrame(data_mongo)


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

if data_frame is not None:
    pH = data_frame['pH'].iloc[0]
    suhu_air =data_frame['suhu'].iloc[0]
    nutrisi = data_frame['tds'].iloc[0]
else:
    st.write('Tidak ada data sensor yang tersedia saat ini.')
    pH, suhu_air, nutrisi = 0, 0, 0

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

if data_frame is not None:


    st.subheader("Choose Machine Learning Model")
    model_option = st.selectbox("Select Model", ("Linear Regression", "Random Forest"))

    if model_option:
        st.success(f"{model_option} selected!")

    st.title("Smart Hidroponik - Prediksi Kesehatan Tanaman")

if 'waktu' in data_frame.columns:
    data_frame['waktu'] = pd.to_datetime(data_frame['waktu'], errors='coerce')


        

    data_frame = data_frame.dropna(subset=['waktu'])
    data_frame['waktu'] = data_frame['waktu'].dt.strftime('%d-%b')

    st.subheader("Grafik Sensor")
    st.write("pH Sensor:")
    st.line_chart(data_frame.set_index('waktu')['pH'])

    st.write("Suhu Air:")
    st.line_chart(data_frame.set_index('waktu')['suhu'])

    st.write("Nutrisi (TDS):")
    st.line_chart(data_frame.set_index('waktu')['tds'])
else:
    st.write("Kolom 'waktu' tidak ditemukan dalam data_frame. Pastikan nama kolom sudah benar.")

def categorize_ph(value):
    if value < 5:
        return 'Rendah'
    elif 5 <= value <= 7:
        return 'Sedang'
    else:
        return 'Tinggi'

def categorize_tds(value):
    if value < 1050:
        return 'Rendah'
    elif 1050 <= value <= 1400:
        return 'Sedang'
    else:
        return 'Tinggi'

data_frame['pH kategori'] = data_frame['pH'].apply(categorize_ph)
data_frame['TDS kategori'] = data_frame['tds'].apply(categorize_tds)

label_encoder = LabelEncoder()
data_frame['TDS kategori'] = label_encoder.fit_transform(data_frame['TDS kategori'])
data_frame['pH kategori'] = label_encoder.fit_transform(data_frame['pH kategori'])

independen_ph = data_frame[['suhu', 'tds']]
dependen_ph = data_frame['pH kategori']
independen_nutrisi = data_frame[['suhu', 'pH']]
dependen_nutrisi = data_frame['TDS kategori']

independen_train_ph, independen_test_ph, dependen_train_ph, dependen_test_ph = train_test_split(independen_ph, dependen_ph, test_size=0.25, stratify=dependen_ph)
independen_train_nutrisi, independen_test_nutrisi, dependen_train_nutrisi, dependen_test_nutrisi = train_test_split(independen_nutrisi, dependen_nutrisi, test_size=0.25, stratify=dependen_nutrisi)

model_ph = LogisticRegression(class_weight='balanced') if model_option == "Linear Regression" else RandomForestClassifier(class_weight='balanced')
model_nutrisi = LogisticRegression(class_weight='balanced') if model_option == "Linear Regression" else RandomForestClassifier(class_weight='balanced')

model_ph.fit(independen_train_ph, dependen_train_ph)
hasil_prediksi_ph = model_ph.predict(independen_test_ph)

model_nutrisi.fit(independen_train_nutrisi, dependen_train_nutrisi)
hasil_prediksi_nutrisi = model_nutrisi.predict(independen_test_nutrisi)

accuracy_ph = accuracy_score(dependen_test_ph, hasil_prediksi_ph)
precision_ph = precision_score(dependen_test_ph, hasil_prediksi_ph, average='macro')
recall_ph = recall_score(dependen_test_ph, hasil_prediksi_ph, average='macro')
f1_ph = f1_score(dependen_test_ph, hasil_prediksi_ph, average='macro')

accuracy_nutrisi = accuracy_score(dependen_test_nutrisi, hasil_prediksi_nutrisi)
precision_nutrisi = precision_score(dependen_test_nutrisi, hasil_prediksi_nutrisi, average='macro')
recall_nutrisi = recall_score(dependen_test_nutrisi, hasil_prediksi_nutrisi, average='macro')
f1_nutrisi = f1_score(dependen_test_nutrisi, hasil_prediksi_nutrisi, average='macro')

# Display the results
st.subheader("Model Evaluation")
st.write(f"Accuracy (pH): {accuracy_ph:.2f}")
st.write(f"Precision (pH): {precision_ph:.2f}")
st.write(f"Recall (pH): {recall_ph:.2f}")
st.write(f"F1 Score (pH): {f1_ph:.2f}")

st.write(f"Accuracy (Nutrisi): {accuracy_nutrisi:.2f}")
st.write(f"Precision (Nutrisi): {precision_nutrisi:.2f}")
st.write(f"Recall (Nutrisi): {recall_nutrisi:.2f}")
st.write(f"F1 Score (Nutrisi): {f1_nutrisi:.2f}")

def show():
        def database:
            client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
            database = client['Smart_Hidroponik']
            koleksi = database['Sensor']
            data = list(koleksi.find())
            return data
        
        def convert_to_csv(df):
            return data_frame.to_csv(index=False).encode('utf-8')
        
        
        st.title('Unduh Sampel Data MongoDB sebagai CSV')
        
        
        data = database()
        
        
        data_frame = pd.DataFrame(data)
        
        
        if '_id' in df.columns:
            df.drop(columns=['_id'], inplace=True)
        
        total_samples = len(df)
        
        
        slide_data_sampel = st.slider("Number of samples", min_value=1, max_value=total_samples, value=min(10, total_samples))
        
        
        generate_button = st.button("Generate CSV")
        
        if generate_button:
        
            df_sample = df.head(num_samples)
            
        
            data_csv = convert_to_csv(df_sample)
            
        
            data_byte = io.BytesIO(data_csv)
            st.download_button(
                label="Unduh CSV",
                data=data_byte,
                file_name='data_sample_smarthidroponik.csv',
                mime='text/csv'
            )
            st.success(f"Data sampel ({slide_data_sampel} baris) berhasil, siap diunduh sebagai CSV!")
show()


