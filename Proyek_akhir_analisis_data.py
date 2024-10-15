import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Membaca dataset
def load_data():
    # Ganti 'order_payments_dataset.csv' dengan path file csv kamu
    df = pd.read_csv('order_payments_dataset.csv')
    return df

# Pastikan kamu memanggil fungsi load_data() dengan tanda kurung
df = load_data()

st.title('Analisis Data Pembayaran Pesanan')

# Menampilkan deskripsi singkat tentang dataset
st.write("""
### Deskripsi Singkat Dataset:
Dataset ini berisi informasi mengenai transaksi pembayaran pesanan, termasuk tipe pembayaran yang digunakan serta nilai pembayaran untuk setiap pesanan.
Beberapa kolom penting dalam dataset ini adalah:
- **order_id**: ID dari pesanan.
- **payment_type**: Jenis metode pembayaran yang digunakan (misal: `credit_card`, `boleto`, dll.).
- **payment_value**: Nilai dari transaksi pembayaran.

Di bawah ini adalah cuplikan dari dataset yang digunakan dalam analisis ini:
""")

# Menampilkan tabel pertama dari dataset
st.dataframe(df.head())

# Checkbox untuk menampilkan seluruh dataset (opsional)
if st.checkbox('Tampilkan seluruh data'):
    st.subheader('Seluruh Dataset')
    st.dataframe(df)

# Sidebar untuk memilih apakah ingin melihat visualisasi
st.sidebar.header('Navigasi Visualisasi:')
visualize_button = st.sidebar.checkbox('Lihat Visualisasi')

# Jika pengguna mengklik tombol untuk melihat visualisasi
if visualize_button:
    # Sidebar untuk memilih tipe visualisasi
    visualization = st.sidebar.selectbox('Pilih Jenis Visualisasi', 
                                         ('Frekuensi Tipe Pembayaran', 'Distribusi Nilai Pembayaran'))

    # Visualisasi Frekuensi Tipe Pembayaran
    if visualization == 'Frekuensi Tipe Pembayaran':
        st.subheader('Visualisasi Frekuensi Penggunaan Tipe Pembayaran')

        # Penjelasan visualisasi
        st.write("""
        **Penjelasan Visualisasi**: 
        Visualisasi ini menunjukkan jumlah transaksi untuk setiap metode pembayaran yang digunakan oleh pelanggan. 
        Dengan grafik ini, kita bisa melihat metode pembayaran yang paling populer di antara pelanggan, 
        dan apakah ada metode tertentu yang jarang digunakan.

        - **Sumbu X**: Tipe pembayaran, misalnya `credit_card`, `boleto`, `voucher`, dll.
        - **Sumbu Y**: Jumlah transaksi yang menggunakan masing-masing tipe pembayaran.
        """)

        # Menghitung frekuensi tipe pembayaran
        payment_type_counts = df['payment_type'].value_counts()

        # Membuat bar plot
        fig, ax = plt.subplots()
        sns.barplot(x=payment_type_counts.index, y=payment_type_counts.values, ax=ax)
        ax.set_xlabel('Tipe Pembayaran')
        ax.set_ylabel('Jumlah Transaksi')
        ax.set_title('Frekuensi Penggunaan Tipe Pembayaran')
        
        # Menampilkan plot di Streamlit
        st.pyplot(fig)

    # Visualisasi Distribusi Nilai Pembayaran (menggunakan box plot)
    elif visualization == 'Distribusi Nilai Pembayaran':
        st.subheader('Visualisasi Distribusi Nilai Pembayaran per Tipe Pembayaran')

        # Penjelasan visualisasi
        st.write("""
        **Penjelasan Visualisasi**: 
        Visualisasi ini menunjukkan distribusi nilai pembayaran untuk setiap tipe pembayaran menggunakan **box plot**. 
        Box plot memberikan informasi tentang persebaran nilai pembayaran, termasuk **median** (nilai tengah), **kuartil** (Q1 dan Q3), 
        serta deteksi **outliers** (nilai yang jauh di luar kisaran normal).
        
        Dalam box plot:
        - **Median (Garis di dalam kotak)**: Nilai tengah dari data. Separuh data berada di atas nilai ini, dan separuh lagi di bawahnya.
        - **Kuartil 1 (Q1)**: Menunjukkan nilai di mana 25% data berada di bawahnya.
        - **Kuartil 3 (Q3)**: Menunjukkan nilai di mana 75% data berada di bawahnya.
        - **Whiskers (Garis vertikal di luar kotak)**: Menunjukkan rentang data utama, di luar itu dianggap outliers.
        - **Outliers (Titik di luar whiskers)**: Nilai pembayaran yang secara signifikan lebih tinggi atau lebih rendah dari distribusi normal.

        **Dengan visualisasi ini, kita dapat melihat:**
        - Apakah suatu metode pembayaran cenderung digunakan untuk pembayaran yang lebih kecil atau lebih besar.
        - Apakah terdapat variasi yang besar dalam nilai pembayaran untuk suatu metode.
        - Deteksi outliers atau transaksi dengan nilai yang ekstrem.
        """)

        # Membuat box plot untuk distribusi nilai pembayaran
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x='payment_type', y='payment_value', data=df, ax=ax)
        ax.set_xlabel('Tipe Pembayaran')
        ax.set_ylabel('Nilai Pembayaran')
        ax.set_title('Distribusi Nilai Pembayaran per Tipe Pembayaran')
        
        # Menampilkan plot di Streamlit
        st.pyplot(fig)

# Menampilkan data mentah (opsional)
if st.checkbox('Tampilkan data mentah'):
    st.subheader('Data Mentah')
    st.write(df)