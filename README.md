# Capital Bikeshare - Data Analysis & Interactive Dashboard

Proyek akhir analisis data Dicoding: **"Belajar Analisis Data dengan Python"**.
Proyek ini melakukan analisis komprehensif terhadap **Bike Sharing Dataset** (Capital Bikeshare, Washington D.C., 2011–2012) mulai dari perumusan pertanyaan bisnis SMART, Data Wrangling, Exploratory Data Analysis (EDA), Visualisasi Data, Analisis Lanjutan (*Manual Grouping Rush Hour* & *Thermal Comfort Binning*), Kesimpulan, hingga pembuatan Dashboard Interaktif menggunakan **Streamlit**.

---

## 👤 Identitas Pengembang
- **Nama:** Umar Faruq Manek
- **Email:** umarfm18@gmail.com
- **ID Dicoding:** umarfaruqmanek

---

## 📁 Struktur Direktori Proyek

```text
submission/
├── dashboard/
│   ├── dashboard.py         # Skrip aplikasi Streamlit interaktif
│   ├── main_data.csv        # Data agregasi harian yang telah dibersihkan
│   └── hour_data.csv        # Data per jam yang telah dibersihkan
├── data/
│   ├── day.csv              # Raw dataset harian
│   └── hour.csv             # Raw dataset per jam
├── notebook.ipynb           # Jupyter Notebook analisis lengkap (berisi output)
├── Proyek_Analisis_Data.ipynb # Berkas salinan notebook sesuai template Dicoding
├── README.md                # Dokumentasi dan panduan menjalankan proyek
├── requirements.txt         # Daftar pustaka/dependensi Python
└── url.txt                  # Tautan dashboard pada Streamlit Cloud
```

---

## 🎯 Pertanyaan Bisnis (SMART Framework)

1. **Pertanyaan 1 (Pengaruh Cuaca & Musim):**
   *Bagaimana pengaruh kondisi cuaca (`weathersit`: cerah, berkabut, hujan/salju ringan) dan musim (`season`: spring, summer, fall, winter) terhadap rata-rata jumlah penyewaan sepeda harian (`cnt`) sepanjang tahun 2011–2012, dan pada kondisi ekstrem seperti apa terjadi penurunan drastis yang memerlukan penyesuaian operasional armada?*
2. **Pertanyaan 2 (Pola Jam Sibuk & Karakteristik Pengguna):**
   *Bagaimana perbedaan pola peminjaman sepeda per jam (`hr`) antara hari kerja (`workingday`) dan hari libur/akhir pekan (`weekend/holiday`), serta bagaimana perbedaan perilaku antara pengguna kasual (`casual`) vs pengguna terdaftar (`registered`) sepanjang tahun 2011–2012 untuk mengoptimalkan ketersediaan unit sepeda di jam-jam sibuk (*peak hours*)?*

---

## ⚙️ Panduan Instalasi & Menjalankan Proyek di Lingkungan Lokal

### 1. Prasyarat
Pastikan komputer Anda telah terinstal **Python 3.9+** (disarankan Python 3.10 atau versi di atasnya) dan `pip`.

### 2. Setup Virtual Environment (Disarankan)

**Pada Windows (Command Prompt / PowerShell):**
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
# Pada PowerShell:
.\venv\Scripts\Activate.ps1
# Atau pada Command Prompt (cmd):
.\venv\Scripts\activate.bat
```

**Pada Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalasi Dependensi
Instal seluruh pustaka yang dibutuhkan menggunakan file `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🚀 Menjalankan Dashboard Streamlit

Untuk menjalankan dashboard secara lokal, buka terminal di direktori utama proyek lalu jalankan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Setelah perintah dijalankan, antarmuka dashboard akan otomatis terbuka di peramban web (*browser*) Anda pada alamat:
`http://localhost:8501`

---

## 📓 Menjalankan Jupyter Notebook

Untuk melihat atau menjalankan kembali seluruh tahapan analisis data langkah-demi-langkah:
```bash
jupyter notebook notebook.ipynb
```
Atau buka file `notebook.ipynb` / `Proyek_Analisis_Data.ipynb` menggunakan **VS Code** atau **Google Colab**. Seluruh sel kode telah dieksekusi lengkap dengan output grafis dan tabel ringkasannya.

---

## 💡 Fitur Utama Dashboard Interaktif
- **Sidebar Filter Dinamis**: Filter rentang tanggal (*date input*), filter pemilihan musim (*season*), dan kondisi cuaca (*weather situation*).
- **Executive Metric Cards**: Menampilkan Total Sewa, Total Kasual, Total Terdaftar, dan Rata-rata Sewa Harian secara responsif sesuai filter.
- **Tab 1 - Dampak Cuaca & Musim**: Visualisasi terstruktur bar plot rata-rata sewa per musim dan cuaca beranotasi nilai.
- **Tab 2 - Pola Jam Sibuk & Profil Pengguna**: Kurva distribusi 24 jam hari kerja vs hari libur dengan highlight area jam sibuk pagi (07:00–09:00) dan sore (16:00–19:00).
- **Tab 3 - Analisis Lanjutan**: Visualisasi segmentasi waktu *Rush Hour Classification* dan *Thermal Comfort Level Binning*.
- **Tab 4 - Kesimpulan & Rekomendasi**: Rangkuman temuan utama serta 4 *action items* strategis operasional bisnis.

---

## 🌐 Deployment ke Streamlit Cloud
Dashboard ini telah aktif dan dapat diakses secara publik pada tautan berikut:
👉 **[https://dashboardpy-xmwcsku3gfibrshsrepx5p.streamlit.app/](https://dashboardpy-xmwcsku3gfibrshsrepx5p.streamlit.app/)**
*(Tautan ini juga telah dicantumkan di dalam berkas `url.txt`).*

