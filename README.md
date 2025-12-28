# Dashboard Prioritas Pembinaan IKM Kota Surabaya

Dashboard ini merupakan implementasi hasil Pemodelan Data Bisnis untuk mendukung
penentuan prioritas pembinaan Industri Kecil dan Menengah (IKM) di Kota Surabaya.

Aplikasi dibangun menggunakan Streamlit dan mengintegrasikan model klasifikasi
skala usaha yang telah dievaluasi dan dilatih ulang menggunakan seluruh data bersih.

## Fitur Utama
- Ringkasan kondisi IKM dan jumlah usaha prioritas pembinaan
- Daftar usaha prioritas pembinaan berdasarkan hasil prediksi skala usaha
- Ringkasan jumlah usaha prioritas per kecamatan
- Simulasi prediksi skala usaha sebagai alat bantu analisis

## Teknologi yang Digunakan
- Python
- scikit-learn
- Streamlit
- Pandas
- NumPy

## Struktur Proyek
- `app.py` : Aplikasi dashboard Streamlit
- `data/` : File output hasil klasifikasi dan pembinaan
- `model/` : Model klasifikasi dan encoder hasil pemodelan
- `notebook/` : Notebook pemodelan dan pengolahan data

## Cara Menjalankan Aplikasi (Lokal dan Publik)
```bash
python -m streamlit run app.py

## Akses Online
https://ikm-app-dashboard-9y6skknrvq2fwtvxt6fgvb.streamlit.app/
