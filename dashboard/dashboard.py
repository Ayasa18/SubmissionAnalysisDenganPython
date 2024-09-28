# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Dashboard Penyewaan Sepeda By Aditiya Saputra")

# Business Objective
st.header("Tujuan Bisnis")
st.write("""
Tujuan dari dashboard ini adalah untuk menganalisis dan memahami pola penyewaan sepeda 
berdasarkan berbagai faktor, termasuk musim, suhu, dan jenis hari (hari kerja vs. libur).
Dengan analisis ini, kita dapat memberikan wawasan yang berguna untuk meningkatkan strategi 
pemasaran dan operasional layanan penyewaan sepeda.
""")

# Key Business Questions
st.header("Pertanyaan Bisnis")
st.write("""
1. Musim mana yang memiliki rata-rata penggunaan sepeda tertinggi?
2. Bagaimana suhu mempengaruhi jumlah penyewaan sepeda?
3. Apa perbedaan rata-rata penyewaan sepeda antara hari kerja dan hari libur?
4. Bagaimana pola penggunaan sepeda per jam pada hari kerja dibandingkan dengan hari libur?
""")

# **Mengimpor Dataset**
main_data = pd.read_csv("./dashboard/main_data.csv")

# Menampilkan data awal
st.title('Analisis Data Penyewaan Sepeda')
st.write(main_data.head())

# **1. Musim apa yang memiliki jumlah penggunaan sepeda tertinggi?**
st.header('1. Musim yang Memiliki Jumlah Penggunaan Sepeda Tertinggi')

# Mengubah angka season menjadi nama musim yang lebih mudah dimengerti
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
main_data['season_name'] = main_data['season_x'].map(season_mapping)

# Menghitung rata-rata penyewaan sepeda per musim
season_avg = main_data.groupby('season_name')['cnt_x'].mean()

# Visualisasi
plt.figure(figsize=(10, 6))
season_avg.plot(kind='bar', color='skyblue')
plt.title('Rata-rata Penggunaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penyewaan Sepeda (cnt)')
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(plt)

# **Analisis Kesimpulan**
st.write("""
Rata-rata penggunaan sepeda menunjukkan bahwa musim Fall (musim gugur) memiliki tingkat penyewaan tertinggi dengan 5644 penyewaan, diikuti oleh musim Summer (musim panas) dengan 4992 penyewaan. 
Sementara itu, musim Winter (musim dingin) dan Spring (musim semi) mencatatkan angka yang lebih rendah, masing-masing dengan 4728 dan 2604 penyewaan. 
Pola ini menunjukkan bahwa kondisi cuaca dan kegiatan luar ruangan pada musim gugur lebih mendukung penggunaan sepeda.
""")

# **2. Bagaimana penyewaan sepeda dipengaruhi oleh suhu?**
st.header('2. Pengaruh Suhu terhadap Penyewaan Sepeda')

# Membagi kolom suhu (temp) ke dalam 5 kategori menggunakan pd.cut
main_data['temp_bin'], bins = pd.cut(main_data['temp_x'],
                                       bins=5,
                                       labels=['Sangat Dingin', 'Dingin', 'Sedang', 'Hangat', 'Panas'],
                                       retbins=True)

# Menghitung rata-rata penyewaan sepeda per kategori suhu
temp_avg = main_data.groupby('temp_bin')['cnt_x'].mean()

# Siapkan data untuk visualisasi
categories = main_data['temp_bin'].cat.categories
temp_ranges = [f"{bins[i]:.2f} - {bins[i + 1]:.2f}°C" for i in range(len(bins) - 1)]
average_counts = temp_avg.values

# Membuat visualisasi
plt.figure(figsize=(10, 6))

# Bar chart untuk rata-rata penyewaan sepeda
bars = plt.bar(categories, average_counts, color='skyblue', alpha=0.7, edgecolor='black')

# Menambahkan teks untuk menunjukkan kisaran suhu di atas grafik
for i, bar in enumerate(bars):
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y + 1, temp_ranges[i], ha='center', color='black')

# Mengatur label dan judul
plt.xlabel('Kategori Suhu', fontsize=12)
plt.ylabel('Rata-rata Penyewaan Sepeda (cnt)', fontsize=12)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu dan Kisaran Suhu', fontsize=16)

# Menampilkan grid
plt.grid(axis='y')

# Menampilkan grafik
st.pyplot(plt)

# **Analisis Kesimpulan**
st.write(""" 
Dari grafik, dapat dilihat bahwa kategori suhu "Hangat" dan "Panas" memiliki jumlah penyewaan sepeda yang tertinggi, 
dengan rata-rata di atas 4.000 penyewaan. Sementara itu, kategori "Sangat Dingin" memiliki rata-rata penyewaan terendah. 
Temuan ini menunjukkan bahwa suhu yang lebih hangat mendorong lebih banyak orang untuk menyewa sepeda, 
yang bisa menjadi dasar untuk strategi pemasaran dan pengelolaan armada sepeda yang lebih efektif di masa mendatang.
""")

# **3. Bagaimana perbandingan penggunaan sepeda antara hari kerja dan hari libur?**
st.header('3. Perbandingan Penggunaan Sepeda: Hari Kerja vs Hari Libur')

# Periksa apakah kolom 'workingday_x' ada di main_data
if 'workingday_x' in main_data.columns:
    # Menghitung rata-rata penyewaan sepeda berdasarkan status hari kerja dan libur
    average_rentals = main_data.groupby('workingday_x')['cnt_x'].mean()

    # Visualisasi
    plt.figure(figsize=(10, 6))
    average_rentals.plot(kind='bar', color='skyblue')
    plt.xticks(ticks=[0, 1], labels=['Libur', 'Hari Kerja'], rotation=0)
    plt.xlabel('Status Hari')
    plt.ylabel('Rata-rata Penyewaan Sepeda (cnt)')
    plt.title('Rata-rata Penyewaan Sepeda: Hari Kerja vs Libur')
    plt.grid(axis='y')

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)

    # **Analisis Kesimpulan**
    st.write(""" 
    Analisis rata-rata penyewaan sepeda berdasarkan status hari menunjukkan bahwa terdapat sedikit perbedaan 
    dalam jumlah penyewaan antara hari kerja dan hari libur. Rata-rata penyewaan sepeda pada hari libur 
    (sekitar {:.2f}) lebih rendah dibandingkan dengan hari kerja (sekitar {:.2f}). 
    Hal ini mengindikasikan bahwa pengguna cenderung lebih banyak menyewa sepeda pada hari kerja, 
    mungkin karena kebutuhan transportasi sehari-hari atau aktivitas di luar ruangan yang lebih tinggi pada hari kerja.
    """.format(average_rentals[0], average_rentals[1]))
else:
    st.warning("Kolom 'workingday_x' tidak ditemukan dalam data yang digabung.")

# **4. Pola Penggunaan Sepeda Setiap Jam: Hari Kerja vs Hari Libur**
st.header('4. Pola Penggunaan Sepeda Setiap Jam: Hari Kerja vs Hari Libur')

# Memisahkan data berdasarkan status hari kerja dan libur
working_day_df = main_data[main_data['workingday_y'] == 1]
holiday_df = main_data[main_data['workingday_y'] == 0]

# Menghitung rata-rata penyewaan sepeda per jam
working_day_hourly_avg = working_day_df.groupby('hr')['cnt_y'].mean()
holiday_hourly_avg = holiday_df.groupby('hr')['cnt_y'].mean()

# Visualisasi
plt.figure(figsize=(12, 6))
plt.plot(working_day_hourly_avg.index, working_day_hourly_avg, label='Hari Kerja', marker='o')
plt.plot(holiday_hourly_avg.index, holiday_hourly_avg, label='Hari Libur', marker='o')
plt.title('Rata-rata Penggunaan Sepeda Berdasarkan Jam: Hari Kerja vs Libur')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Penyewaan Sepeda (cnt)')
plt.xticks(range(0, 24))  # Menampilkan setiap jam dari 0 hingga 23
plt.legend()
plt.grid()
st.pyplot(plt)

# **Analisis Kesimpulan**
st.write(""" 
Berdasarkan grafik, terdapat perbedaan pola penyewaan yang jelas antara hari kerja dan hari libur. 
Pada hari kerja, penggunaan sepeda menunjukkan puncaknya pada jam-jam awal pagi dan sore, 
sedangkan di hari libur cenderung lebih merata sepanjang hari. 
Angka penyewaan di hari libur umumnya lebih rendah dibandingkan dengan hari kerja, 
yang mengindikasikan bahwa faktor kerja memiliki pengaruh signifikan terhadap pola penyewaan sepeda.
""")
