import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ---------------------------------------------------------
# 1. Konfigurasi Halaman & Desain Dasar
# ---------------------------------------------------------
st.set_page_config(
    page_title="Capital Bikeshare Analytics Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan yang elegan dan modern
st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #4B5563;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #F8FAFC;
            border-radius: 10px;
            padding: 15px;
            border-left: 5px solid #2563EB;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .insight-box {
            background-color: #EFF6FF;
            border-left: 4px solid #3B82F6;
            padding: 14px 18px;
            border-radius: 6px;
            margin-top: 15px;
            margin-bottom: 20px;
            font-size: 0.95rem;
            color: #1E3A8A;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Pemuatan Data dengan Caching
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(base_dir, 'main_data.csv')
    hour_path = os.path.join(base_dir, 'hour_data.csv')

    # Fallback paths
    if not os.path.exists(main_path):
        main_path = 'main_data.csv' if os.path.exists('main_data.csv') else 'dashboard/main_data.csv'
    if not os.path.exists(hour_path):
        hour_path = 'hour_data.csv' if os.path.exists('hour_data.csv') else 'dashboard/hour_data.csv'

    df_day = pd.read_csv(main_path)
    df_hour = pd.read_csv(hour_path)

    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

    return df_day, df_hour

try:
    df_day, df_hour = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# ---------------------------------------------------------
# 3. Sidebar Interaktif (Filter & Profil Pengguna)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("🚲 Filter Dashboard")
    st.markdown("Sesuaikan parameter di bawah untuk memfilter data operasional:")

    # Filter Rentang Tanggal
    min_date = df_day['dteday'].min().date()
    max_date = df_day['dteday'].max().date()
    
    date_range = st.date_input(
        "📅 Rentang Tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Validasi input rentang tanggal
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = min_date
        end_date = max_date

    # Filter Musim (Season)
    available_seasons = list(df_day['season_label'].unique())
    selected_seasons = st.multiselect(
        "🍂 Pilih Musim (Season):",
        options=available_seasons,
        default=available_seasons
    )

    # Filter Kondisi Cuaca (Weather Situation)
    available_weather = list(df_day['weather_label'].unique())
    selected_weather = st.multiselect(
        "🌦️ Pilih Kondisi Cuaca:",
        options=available_weather,
        default=available_weather
    )

    st.markdown("---")
    st.markdown("**Profil Analis:**")
    st.markdown("👤 **Umar Faruq Manek**")
    st.markdown("📧 *umarfm18@gmail.com*")
    st.markdown("🆔 Dicoding: *umarfaruqmanek*")

# ---------------------------------------------------------
# 4. Filter Data Berdasarkan Pilihan Sidebar
# ---------------------------------------------------------
filtered_day = df_day[
    (df_day['dteday'].dt.date >= start_date) &
    (df_day['dteday'].dt.date <= end_date) &
    (df_day['season_label'].isin(selected_seasons)) &
    (df_day['weather_label'].isin(selected_weather))
]

filtered_hour = df_hour[
    (df_hour['dteday'].dt.date >= start_date) &
    (df_hour['dteday'].dt.date <= end_date) &
    (df_hour['season_label'].isin(selected_seasons)) &
    (df_hour['weather_label'].isin(selected_weather))
]

# ---------------------------------------------------------
# 5. Header & Ringkasan Metrik Utama (KPIs)
# ---------------------------------------------------------
st.markdown('<div class="main-header">Capital Bikeshare Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Analisis Perilaku Pengguna, Pola Jam Sibuk, dan Dampak Cuaca Periode {start_date} s/d {end_date}</div>', unsafe_allow_html=True)

if filtered_day.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi filter yang dipilih. Silakan atur kembali filter di sidebar.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

total_rentals = filtered_day['cnt'].sum()
total_casual = filtered_day['casual'].sum()
total_registered = filtered_day['registered'].sum()
avg_daily = filtered_day['cnt'].mean()

with col1:
    st.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,.0f}")
with col2:
    pct_casual = (total_casual / total_rentals * 100) if total_rentals > 0 else 0
    st.metric(label="Pengguna Kasual (Casual)", value=f"{total_casual:,.0f}", delta=f"{pct_casual:.1f}% Total")
with col3:
    pct_reg = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
    st.metric(label="Pengguna Terdaftar (Registered)", value=f"{total_registered:,.0f}", delta=f"{pct_reg:.1f}% Total")
with col4:
    st.metric(label="Rata-rata Sewa Harian", value=f"{avg_daily:,.0f} unit/hari")

st.markdown("---")

# ---------------------------------------------------------
# 6. Tab Visualisasi Interaktif
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🌦️ Dampak Cuaca & Musim (Pertanyaan 1)",
    "⏰ Pola Jam Sibuk & Tipe Pengguna (Pertanyaan 2)",
    "📊 Analisis Lanjutan (Clustering/Binning)",
    "💡 Kesimpulan & Rekomendasi Aksi"
])

# ---------------------------------------------------------
# TAB 1: Dampak Cuaca & Musim (Pertanyaan 1)
# ---------------------------------------------------------
with tab1:
    st.subheader("Pengaruh Pergantian Musim & Kondisi Cuaca terhadap Penyewaan")
    st.markdown("Visualisasi ini menjawab **Pertanyaan Bisnis 1**: Mengukur bagaimana faktor iklim dan cuaca memengaruhi fluktuasi rata-rata peminjaman sepeda harian.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🍂 Rata-rata Penyewaan per Musim")
        season_agg = filtered_day.groupby('season_label')['cnt'].mean().reset_index()
        season_order = [s for s in ['Spring', 'Summer', 'Fall', 'Winter'] if s in season_agg['season_label'].values]
        
        fig_season, ax_season = plt.subplots(figsize=(7, 4.5))
        palette_s = {'Spring': '#bdc3c7', 'Summer': '#3498db', 'Fall': '#e67e22', 'Winter': '#95a5a6'}
        sns.barplot(
            data=season_agg,
            x='season_label',
            y='cnt',
            order=season_order,
            hue='season_label',
            palette=palette_s,
            legend=False,
            ax=ax_season
        )
        ax_season.set_ylabel("Rata-rata Sewa (Unit / Hari)")
        ax_season.set_xlabel("Musim")
        for p in ax_season.patches:
            val = p.get_height()
            ax_season.annotate(f"{val:,.0f}", (p.get_x() + p.get_width() / 2., val),
                               ha='center', va='bottom', xytext=(0, 4), textcoords='offset points',
                               fontweight='bold', fontsize=10, color='#2c3e50')
        plt.tight_layout()
        st.pyplot(fig_season)

    with c2:
        st.markdown("#### 🌦️ Rata-rata Penyewaan per Kondisi Cuaca")
        weather_agg = filtered_day.groupby('weather_label')['cnt'].mean().reset_index()
        weather_order = [w for w in ['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Rain'] if w in weather_agg['weather_label'].values]
        
        fig_weather, ax_weather = plt.subplots(figsize=(7, 4.5))
        palette_w = {'Clear/Partly Cloudy': '#27ae60', 'Mist/Cloudy': '#f39c12', 'Light Snow/Rain': '#c0392b'}
        sns.barplot(
            data=weather_agg,
            x='weather_label',
            y='cnt',
            order=weather_order,
            hue='weather_label',
            palette=palette_w,
            legend=False,
            ax=ax_weather
        )
        ax_weather.set_ylabel("Rata-rata Sewa (Unit / Hari)")
        ax_weather.set_xlabel("Kondisi Cuaca")
        for p in ax_weather.patches:
            val = p.get_height()
            ax_weather.annotate(f"{val:,.0f}", (p.get_x() + p.get_width() / 2., val),
                               ha='center', va='bottom', xytext=(0, 4), textcoords='offset points',
                               fontweight='bold', fontsize=10, color='#2c3e50')
        plt.tight_layout()
        st.pyplot(fig_weather)

    st.markdown("""
        <div class="insight-box">
            <b>Insight Analisis Cuaca & Musim:</b><br>
            • Musim gugur (<b>Fall</b>) menjadi periode dengan permintaan tertinggi (~5.644 unit/hari), sedangkan musim semi (<b>Spring</b>) terendah (~2.604 unit/hari).<br>
            • Cuaca presipitasi buruk (<b>Light Snow/Rain</b>) mengakibatkan anjloknya penyewaan sebesar <b>63%</b> dibandingkan hari cerah. Hal ini membuktikan pentingnya kesiapan mitigasi operasional dan penyesuaian target armada saat cuaca buruk diprediksi BMKG lokal.
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: Pola Jam Sibuk & Tipe Pengguna (Pertanyaan 2)
# ---------------------------------------------------------
with tab2:
    st.subheader("Dinamika Jam Sibuk Komuter vs Rekreasi Akhir Pekan")
    st.markdown("Visualisasi ini menjawab **Pertanyaan Bisnis 2**: Mengidentifikasi jam puncak operasional (*peak hours*) dan membedah disparitas perilaku antara pengguna terdaftar (komuter) dan kasual (rekreasional).")

    fig_hour, axes_hour = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

    # Plot 1: Pola Hari Kerja vs Hari Libur
    work_agg = filtered_hour[filtered_hour['workingday'] == 1].groupby('hr')['cnt'].mean()
    non_work_agg = filtered_hour[filtered_hour['workingday'] == 0].groupby('hr')['cnt'].mean()

    if not work_agg.empty:
        axes_hour[0].plot(work_agg.index, work_agg.values, label='Hari Kerja (Working Day)', color='#1f77b4', linewidth=2.5, marker='o')
    if not non_work_agg.empty:
        axes_hour[0].plot(non_work_agg.index, non_work_agg.values, label='Hari Libur / Akhir Pekan', color='#ff7f0e', linewidth=2.5, marker='s')

    axes_hour[0].axvspan(7, 9, color='#1f77b4', alpha=0.15, label='Morning Peak (07:00-09:00)')
    axes_hour[0].axvspan(16, 19, color='#d62728', alpha=0.15, label='Evening Peak (16:00-19:00)')
    axes_hour[0].set_title("Pola Distribusi Penyewaan per Jam: Hari Kerja vs Akhir Pekan", pad=10)
    axes_hour[0].set_ylabel("Rata-rata Sewa (Unit / Jam)")
    axes_hour[0].legend(loc='upper left')
    axes_hour[0].set_xticks(range(0, 24))

    # Plot 2: Pengguna Kasual vs Terdaftar
    cas_agg = filtered_hour.groupby('hr')['casual'].mean()
    reg_agg = filtered_hour.groupby('hr')['registered'].mean()

    axes_hour[1].plot(reg_agg.index, reg_agg.values, label='Pengguna Terdaftar (Registered Commuters)', color='#27ae60', linewidth=2.5, marker='^')
    axes_hour[1].plot(cas_agg.index, cas_agg.values, label='Pengguna Kasual (Casual Riders)', color='#e74c3c', linewidth=2.5, marker='d')
    axes_hour[1].set_title("Perbandingan Profil Pengguna per Jam (Terdaftar vs Kasual)", pad=10)
    axes_hour[1].set_xlabel("Jam Operasional (0 - 23)")
    axes_hour[1].set_ylabel("Rata-rata Sewa (Unit / Jam)")
    axes_hour[1].legend(loc='upper left')
    axes_hour[1].set_xticks(range(0, 24))

    plt.tight_layout()
    st.pyplot(fig_hour)

    st.markdown("""
        <div class="insight-box">
            <b>Insight Pola Jam Sibuk & Segmentasi Pengguna:</b><br>
            • <b>Hari Kerja (Pola Bimodal):</b> Lonjakan peminjaman terkonsentrasi sangat tinggi pada pukul <b>08:00 pagi</b> (477 unit/jam) dan <b>17:00–18:00 sore</b> (525 unit/jam), digerakkan secara masif oleh pekerja komuter terdaftar.<br>
            • <b>Hari Libur (Pola Unimodal):</b> Aktivitas naik secara perlahan sejak jam 10:00 dan mencapai puncak santai pada siang hingga sore hari pukul <b>12:00–16:00</b>, dengan kontribusi tinggi dari pengguna kasual.
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: Analisis Lanjutan (Clustering/Binning)
# ---------------------------------------------------------
with tab3:
    st.subheader("Teknik Analisis Lanjutan: Manual Grouping & Binning")
    st.markdown("""
        Penerapan analisis lanjutan relevan tanpa machine learning guna mengklasifikasikan beban operasional armada:
        1. **Manual Grouping Waktu (*Rush Hour Classification*)**: Mengelompokkan 24 jam menjadi segmen *Morning Rush*, *Midday*, *Evening Rush*, dan *Night/Off-Peak*.
        2. **Binning Kenyamanan Suhu (*Thermal Comfort Level*)**: Mengelompokkan suhu (°C) menjadi *Dingin*, *Sejuk*, *Hangat/Ideal*, dan *Panas*.
    """)

    cl1, cl2 = st.columns(2)

    with cl1:
        st.markdown("#### ⏳ Akumulasi Sewa Berdasarkan Segmen Jam")
        order_rush = ['Morning Rush (07:00-09:00)', 'Midday (10:00-15:00)', 'Evening Rush (16:00-19:00)', 'Night/Off-Peak (20:00-06:00)']
        rush_data = filtered_hour.groupby(['rush_hour_group', 'day_type'])['cnt'].sum().reset_index()

        fig_rush, ax_rush = plt.subplots(figsize=(7, 5))
        sns.barplot(
            data=rush_data,
            x='rush_hour_group',
            y='cnt',
            hue='day_type',
            order=[r for r in order_rush if r in rush_data['rush_hour_group'].values],
            palette=['#e74c3c', '#3498db'],
            ax=ax_rush
        )
        ax_rush.set_title("Total Volume Sewa per Segmen Waktu")
        ax_rush.set_ylabel("Total Sewa (Unit)")
        ax_rush.set_xlabel("Segmen Jam Operasional")
        ax_rush.set_xticks(range(len(order_rush)))
        ax_rush.set_xticklabels(['Morning\\n(07-09)', 'Midday\\n(10-15)', 'Evening\\n(16-19)', 'Night\\n(20-06)'])
        ax_rush.legend(title="Tipe Hari", loc='upper right')
        plt.tight_layout()
        st.pyplot(fig_rush)

    with cl2:
        st.markdown("#### 🌡️ Rata-rata Sewa Berdasarkan Kategori Suhu")
        order_temp = ['Dingin (<12°C)', 'Sejuk (12-20°C)', 'Hangat/Ideal (20-28°C)', 'Panas (>28°C)']
        temp_data = filtered_hour.groupby('temp_group', observed=False)['cnt'].mean().reset_index()

        fig_temp, ax_temp = plt.subplots(figsize=(7, 5))
        sns.barplot(
            data=temp_data,
            x='temp_group',
            y='cnt',
            order=[t for t in order_temp if t in temp_data['temp_group'].values],
            hue='temp_group',
            palette='YlOrRd',
            legend=False,
            ax=ax_temp
        )
        ax_temp.set_title("Rata-rata Sewa per Jam Berdasarkan Suhu")
        ax_temp.set_ylabel("Rata-rata Sewa (Unit / Jam)")
        ax_temp.set_xlabel("Kategori Kenyamanan Suhu")
        for p in ax_temp.patches:
            val = p.get_height()
            ax_temp.annotate(f"{val:,.1f}", (p.get_x() + p.get_width() / 2., val),
                             ha='center', va='bottom', xytext=(0, 4), textcoords='offset points',
                             fontweight='bold', fontsize=10, color='#2c3e50')
        plt.tight_layout()
        st.pyplot(fig_temp)

    st.markdown("""
        <div class="insight-box">
            <b>Insight Analisis Lanjutan:</b><br>
            • <b>Evening Rush (16:00–19:00):</b> Menjadi segmen dengan akumulasi volume sewa tertinggi pada hari kerja (>827 ribu unit), menandakan titik beban logistik paling kritis di mana risiko kehabisan dermaga (dock saturation) paling sering terjadi.<br>
            • <b>Dinamika Termal:</b> Peminjaman sepeda melonjak tajam seiring kenaikan suhu, mencapai rata-rata <b>306,7 unit/jam</b> pada suhu panas (>28°C), berbanding hanya <b>77,3 unit/jam</b> saat suhu dingin (<12°C).
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: Kesimpulan & Rekomendasi Aksi
# ---------------------------------------------------------
with tab4:
    st.subheader("Kesimpulan & Rekomendasi Action Item Bisnis")

    st.markdown("### 📌 Kesimpulan Analisis Data")
    st.markdown("""
        1. **Kesimpulan Pertanyaan 1 (Dampak Cuaca & Musim):**
           - Permintaan sewa sangat dipengaruhi musim, dengan puncak tertinggi di **Musim Gugur (Fall: 5.644 sewa/hari)** dan terendah di **Musim Semi (Spring: 2.604 sewa/hari)**.
           - Cuaca hujan/salju (*Light Snow/Rain*) merontokkan permintaan hingga **63,02%** dibandingkan hari cerah.
        2. **Kesimpulan Pertanyaan 2 (Pola Jam & Tipe Pengguna):**
           - Hari kerja memperlihatkan pola *bimodal* dengan jam sibuk komuter pukul **08:00** dan **17:00–18:00** yang didominasi oleh pengguna *registered*.
           - Akhir pekan memperlihatkan pola *unimodal* santai dengan jam puncak pukul **12:00–16:00** yang didominasi oleh pengguna *casual*.
        3. **Kesimpulan Analisis Lanjutan:**
           - Jam sibuk sore hari (*Evening Rush*) merupakan pusat konsentrasi pemakaian terbesar.
           - Suhu hangat/panas (>20°C) menjadi pemicu peningkatan mobilitas terbesar bagi pesepeda kasual.
    """)

    st.markdown("---")
    st.markdown("### 🚀 Rekomendasi Action Item Strategis")

    r1, r2 = st.columns(2)
    with r1:
        st.info("""
            **1. Dynamic Dock Rebalancing (Jam Sibuk Komuter):**
            - Mobilisasi truk logistik armada pada pukul **06:30–07:30** untuk mengisi stasiun di area permukiman komuter, dan pukul **15:30–16:30** untuk mengosongkan/menyeimbangkan stasiun di area perkantoran sebelum jam pulang kantor (17:00).
        """)
        st.success("""
            **2. Seasonal Preventive Maintenance (Perawatan Musiman):**
            - Lakukan overhaul, rotasi, dan servis suku cadang besar-besaran saat **Musim Dingin (Desember–Februari)** saat permintaan sewa paling rendah, agar seluruh armada 100% siap di musim panas dan gugur.
        """)

    with r2:
        st.warning("""
            **3. Weekend-to-Commuter Conversion Marketing:**
            - Luncurkan promo diskon langganan tahunan *(Weekend Pass to Annual Membership)* khusus kepada pengguna kasual yang aktif di akhir pekan dan siang hari, guna mengamankan pendapatan berulang *(recurring revenue)*.
        """)
        st.error("""
            **4. Crowdsourced Rebalancing Gamification:**
            - Berikan reward poin atau kredit gratis bagi pengguna yang mengambil sepeda dari stasiun penuh dan mengembalikannya ke stasiun yang kekurangan armada di jam-jam sibuk.
        """)

st.caption("Dicoding Data Analysis Final Project Submission | Author: Umar Faruq Manek")

