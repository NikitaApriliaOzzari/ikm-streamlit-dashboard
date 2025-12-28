import streamlit as st
import pandas as pd
import numpy as np
import joblib

# PAGE CONFIG
st.set_page_config(
    page_title="Dashboard Pembinaan IKM",
    layout="wide"
)

st.title("Dashboard Prioritas Pembinaan IKM Kota Surabaya")
st.caption("Implementasi Pemodelan Data Bisnis")

# LOAD DATA
@st.cache_data
def load_data():
    hasil = pd.read_excel("data/hasil_klasifikasi_skala_usaha_lengkap.xlsx")
    prioritas = pd.read_excel("data/prioritas_pembinaan_ikm_lengkap.xlsx")
    kecamatan = pd.read_excel("data/prioritas_kecamatan_pembinaan.xlsx")
    return hasil, prioritas, kecamatan

hasil, prioritas, kecamatan = load_data()

# LOAD MODEL & ENCODER
@st.cache_resource
def load_model():
    model = joblib.load("model/decision_tree.pkl")
    encoder = joblib.load("model/encoder.pkl")
    return model, encoder

model, encoder = load_model()


# KONTRAK KOLOM 
NUM_COLS = [
    "Jumlah Investasi",
    "Luas Tanah",
    "TKI"
]

CAT_COLS = list(encoder.feature_names_in_)  

# TABS
tab1, tab2, tab3 = st.tabs([
    "Ringkasan & Kecamatan",
    "Usaha Prioritas",
    "Simulasi Prediksi"
])

# TAB 1 — RINGKASAN
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total IKM", hasil.shape[0])
    col2.metric("Usaha Prioritas", prioritas.shape[0])
    col3.metric("Jumlah Kecamatan", kecamatan.shape[0])

    st.subheader("Prioritas Pembinaan per Kecamatan")
    st.dataframe(kecamatan, use_container_width=True)

# TAB 2 — USAHA PRIORITAS
with tab2:
    st.subheader("Daftar Usaha Prioritas Pembinaan")

    kec_filter = st.selectbox(
        "Filter Kecamatan",
        ["Semua"] + sorted(prioritas["Kecamatan"].dropna().unique())
    )

    if kec_filter != "Semua":
        view = prioritas[prioritas["Kecamatan"] == kec_filter]
    else:
        view = prioritas

    st.dataframe(view, use_container_width=True)

# TAB 3 — SIMULASI PREDIKSI
with tab3:
    st.subheader("Simulasi Prediksi Skala Usaha")
    st.caption("Hasil simulasi bersifat alat bantu, bukan penetapan resmi.")

    # ---------- INPUT NUMERIK ----------
    investasi = st.number_input(
        "Jumlah Investasi (Rp)",
        min_value=0.0,
        value=50_000_000.0
    )

    luas = st.number_input(
        "Luas Tanah (m²)",
        min_value=0.0,
        value=50.0
    )

    tki = st.number_input(
        "Jumlah TKI",
        min_value=1,
        value=1
    )

    # ---------- INPUT KATEGORIK (DARI ENCODER) ----------
    cat_values = {}
    for i, col in enumerate(CAT_COLS):
        cat_values[col] = st.selectbox(
            col,
            encoder.categories_[i]
        )

    # ---------- PREDIKSI ----------
    if st.button("Prediksi"):
        
        input_df = pd.DataFrame([{
            "Jumlah Investasi": investasi,
            "Luas Tanah": luas,
            "TKI": tki,
            **cat_values
        }])

        # VALIDASI KERAS
        missing = set(CAT_COLS + NUM_COLS) - set(input_df.columns)
        if missing:
            st.error(f"Kolom hilang: {missing}")
            st.stop()

        # TRANSFORM
        X_cat = encoder.transform(input_df[CAT_COLS])
        X_num = input_df[NUM_COLS].values
        X_sim = np.hstack([X_num, X_cat])

        # PREDIKSI
        pred = model.predict(X_sim)[0]

        st.success(f"Prediksi Skala Usaha: **{pred}**")
