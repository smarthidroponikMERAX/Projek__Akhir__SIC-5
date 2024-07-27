import streamlit as st
import pandas as pd
from pymongo import MongoClient
import io

def show():
        def database():
            client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
            database = client['Smart_Hidroponik']
            koleksi = database['Sensor']
            data = list(koleksi.find())
            return data
        
        def convert_to_csv(data_frame):
            return data_frame.to_csv(index=False).encode('utf-8')
        
        
        st.title('Unduh Sampel Data MongoDB sebagai CSV')
        
        
        data = database()
        
        
        data_frame = pd.DataFrame(data)
        
        
        if '_id' in data_frame.columns:
            data_frame.drop(columns=['_id'], inplace=True)
        
        total_samples = len(df)
        
        
        slide_data_sampel = st.slider("Number of samples", min_value=1, max_value=total_samples, value=min(10, total_samples))
        
        
        generate_button = st.button("Generate CSV")
        
        if generate_button:
        
            df_sample = data_frame.head(num_samples)
            
        
            data_csv = convert_to_csv(df_sample)
            
        
            data_byte = io.BytesIO(data_csv)
            st.download_button(
                label="Unduh CSV",
                data=data_byte,
                file_name='data_sample_smarthidroponik.csv',
                mime='text/csv'
            )
            st.success(f"Data sampel ({slide_data_sampel} baris) berhasil, siap diunduh sebagai CSV!")
