import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Membaca dataset
@st.cache_data
def load_data():
    # Ganti 'order_payments_dataset.csv' dengan path file csv kamu
    df = pd.read_csv('OrderTypeAnalisis/order_payments_dataset.csv')
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
- **payment_sequential**: Nomor urut pembayaran untuk pesanan tertentu.
- **payment_installments**: Jumlah pembayaran yang dibagi-bagi untuk pesanan tertentu.

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
    visualization = st.sidebar.radio('Pilih Jenis Visualisasi', 
                                     ('Frekuensi Tipe Pembayaran', 'Distribusi Nilai Pembayaran', 
                                      'Total Nilai Pembayaran per Tipe Pembayaran', 'Rata-rata Nilai Pembayaran per Tipe Pembayaran',
                                      'Distribusi Jumlah Cicilan Pembayaran'))

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

        payment_type_counts = df['payment_type'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=payment_type_counts.index, y=payment_type_counts.values, palette='viridis', ax=ax, hue=payment_type_counts.index, legend=False)
        ax.set_xlabel('Tipe Pembayaran')
        ax.set_ylabel('Jumlah Transaksi')
        ax.set_title('Frekuensi Penggunaan Tipe Pembayaran')
        # Menambahkan anotasi tiap batang
        for i, v in enumerate(payment_type_counts.values):
            ax.text(i, v + 0.5, str(v), color='black', ha='center')
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
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(x='payment_type', y='payment_value', data=df, palette='Set2', ax=ax, hue='payment_type', legend=False)
        sns.swarmplot(x='payment_type', y='payment_value', data=df, color='k', size=3, ax=ax)
        ax.set_xlabel('Tipe Pembayaran')
        ax.set_ylabel('Nilai Pembayaran')
        ax.set_title('Distribusi Nilai Pembayaran per Tipe Pembayaran')
        st.pyplot(fig)

    # Visualisasi Total Nilai Pembayaran per Tipe Pembayaran
    elif visualization == 'Total Nilai Pembayaran per Tipe Pembayaran':
        st.subheader('Visualisasi Total Nilai Pembayaran per Tipe Pembayaran')

        # Penjelasan visualisasi
        st.write("""
        **Penjelasan Visualisasi**: 
        Visualisasi ini menunjukkan total nilai pembayaran untuk setiap metode pembayaran yang digunakan oleh pelanggan. 
        Dengan grafik ini, kita bisa melihat metode pembayaran mana yang menghasilkan nilai transaksi terbesar.

        - **Sumbu X**: Tipe pembayaran, misalnya `credit_card`, `boleto`, `voucher`, dll.
        - **Sumbu Y**: Total nilai pembayaran yang menggunakan masing-masing tipe pembayaran.
        """)

        total_payment_value = df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=total_payment_value.values, y=total_payment_value.index, palette='coolwarm', ax=ax)
        ax.set_xlabel('Total Nilai Pembayaran')
        ax.set_ylabel('Tipe Pembayaran')
        ax.set_title('Total Nilai Pembayaran per Tipe Pembayaran')
        for i, v in enumerate(total_payment_value.values):
            ax.text(v + max(total_payment_value.values)*0.01, i, str(round(v, 2)), color='black', va='center')
        st.pyplot(fig)

    # Visualisasi Rata-rata Nilai Pembayaran per Tipe Pembayaran
    elif visualization == 'Rata-rata Nilai Pembayaran per Tipe Pembayaran':
        st.subheader('Visualisasi Rata-rata Nilai Pembayaran per Tipe Pembayaran')

        # Penjelasan visualisasi
        st.write("""
        **Penjelasan Visualisasi**: 
        Visualisasi ini menunjukkan nilai rata-rata pembayaran untuk setiap metode pembayaran yang digunakan oleh pelanggan. 
        Dengan grafik ini, kita bisa melihat metode pembayaran mana yang cenderung digunakan untuk transaksi dengan nilai yang lebih tinggi atau lebih rendah.

        - **Sumbu X**: Tipe pembayaran, misalnya `credit_card`, `boleto`, `voucher`, dll.
        - **Sumbu Y**: Rata-rata nilai pembayaran yang menggunakan masing-masing tipe pembayaran.
        """)

        avg_payment_value = df.groupby('payment_type')['payment_value'].mean().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=avg_payment_value.values, y=avg_payment_value.index, palette='magma', ax=ax)
        ax.set_xlabel('Rata-rata Nilai Pembayaran')
        ax.set_ylabel('Tipe Pembayaran')
        ax.set_title('Rata-rata Nilai Pembayaran per Tipe Pembayaran')
        for i, v in enumerate(avg_payment_value.values):
            ax.text(v + max(avg_payment_value.values)*0.01, i, str(round(v, 2)), color='black', va='center')
        st.pyplot(fig)

    # Visualisasi Distribusi Jumlah Cicilan Pembayaran
    elif visualization == 'Distribusi Jumlah Cicilan Pembayaran':
        st.subheader('Visualisasi Distribusi Jumlah Cicilan Pembayaran per Tipe Pembayaran')

        # Penjelasan visualisasi
        st.write("""
        **Penjelasan Visualisasi**: 
        Visualisasi ini menunjukkan distribusi jumlah cicilan pembayaran untuk setiap tipe pembayaran menggunakan **box plot**. 
        Box plot memberikan informasi tentang persebaran jumlah cicilan, termasuk **median** (nilai tengah), **kuartil** (Q1 dan Q3), 
        serta deteksi **outliers** (nilai yang jauh di luar kisaran normal).
        
        Dalam box plot:
        - **Median (Garis di dalam kotak)**: Nilai tengah dari data. Separuh data berada di atas nilai ini, dan separuh lagi di bawahnya.
        - **Kuartil 1 (Q1)**: Menunjukkan nilai di mana 25% data berada di bawahnya.
        - **Kuartil 3 (Q3)**: Menunjukkan nilai di mana 75% data berada di bawahnya.
        - **Whiskers (Garis vertikal di luar kotak)**: Menunjukkan rentang data utama, di luar itu dianggap outliers.
        - **Outliers (Titik di luar whiskers)**: Jumlah cicilan yang secara signifikan lebih tinggi atau lebih rendah dari distribusi normal.

        **Dengan visualisasi ini, kita dapat melihat:**
        - Apakah suatu metode pembayaran cenderung digunakan untuk pembayaran dengan cicilan yang lebih banyak atau lebih sedikit.
        - Apakah terdapat variasi yang besar dalam jumlah cicilan untuk suatu metode.
        - Deteksi outliers atau transaksi dengan jumlah cicilan yang ekstrem.
        """)

        # Membuat box plot untuk distribusi jumlah cicilan pembayaran
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(x='payment_installments', y='payment_type', data=df, palette='Pastel1', ax=ax)
        ax.set_xlabel('Jumlah Cicilan')
        ax.set_ylabel('Tipe Pembayaran')
        ax.set_title('Distribusi Jumlah Cicilan Pembayaran per Tipe Pembayaran')
        st.pyplot(fig)