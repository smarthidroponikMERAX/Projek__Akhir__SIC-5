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

st.set_page_config(page_title='Smart Hidroponik',layout="wide", page_icon="🌿") 
