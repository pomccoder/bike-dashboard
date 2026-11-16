import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman dashboard
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_style("whitegrid")

# Fungsi memuat data (aman dijalankan dari root folder maupun dari dalam folder dashboard/)
@st.cache_data
def load_data():
    file_path = "dashboard/main_data.csv" if os.path.exists("dashboard/main_data.csv") else "main_data.csv"
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])

    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cluster_order = [
        'Night (00:00-05:59)',
        'Morning (06:00-11:59)',
        'Afternoon (12:00-17:59)',
        'Evening (18:00-23:59)'
    ]

    df['season'] = pd.Categorical(df['season'], categories=season_order, ordered=True)
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    if 'time_cluster' in df.columns:
        df['time_cluster'] = pd.Categorical(df['time_cluster'], categories=cluster_order, ordered=True)

    return df

df = load_data()

# --- SIDEBAR FILTER ---
with st.sidebar:
    st.title("🚲 Capital Bikeshare")
    st.markdown("**Filter Eksplorasi Data**")

    min_date = df['dteday'].min().date()
    max_date = df['dteday'].max().date()

    date_range = st.date_input(
        label="Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    selected_seasons = st.multiselect(
        label="Pilih Musim (Season)",
        options=['Spring', 'Summer', 'Fall', 'Winter'],
        default=['Spring', 'Summer', 'Fall', 'Winter']
    )

    selected_workingday = st.multiselect(
        label="Pilih Tipe Hari",
        options=['Working Day', 'Weekend/Holiday'],
        default=['Working Day', 'Weekend/Holiday']
    )

# Validasi rentang tanggal
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered_df = df[
    (df['dteday'].dt.date >= start_date) &
    (df['dteday'].dt.date <= end_date) &
    (df['season'].isin(selected_seasons)) &
    (df['workingday'].isin(selected_workingday))
]

# Agregasi harian dari data terfilter
daily_df = filtered_df.groupby(
    ['dteday', 'season', 'day_weathersit', 'year', 'month', 'workingday'],
    observed=True
).agg(
    total_count=('total_count', 'sum'),
    casual=('casual', 'sum'),
    registered=('registered', 'sum')
).reset_index()

# --- HEADER & KPI METRICS ---
st.title("🚲 Bike Sharing Data Analysis Dashboard (2011–2012)")
st.markdown("Dashboard interaktif untuk mengevaluasi pengaruh cuaca, perilaku pengguna per jam, dan pertumbuhan penyewaan sepeda di Washington D.C.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewaan", f"{filtered_df['total_count'].sum():,}")
with col2:
    st.metric("Pengguna Registered", f"{filtered_df['registered'].sum():,}")
with col3:
    st.metric("Pengguna Casual", f"{filtered_df['casual'].sum():,}")
with col4:
    avg_daily = daily_df['total_count'].mean() if not daily_df.empty else 0
    st.metric("Rata-rata Harian", f"{avg_daily:,.0f} unit/hari")

st.divider()

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan kombinasi filter yang dipilih. Silakan ubah filter pada sidebar.")
    st.stop()

# --- PERTANYAAN 1: PENGARUH MUSIM & CUACA ---
st.subheader("1. Pengaruh Musim dan Kondisi Cuaca terhadap Rata-rata Penyewaan Harian")
fig1, axes1 = plt.subplots(1, 2, figsize=(15, 5.5))

season_avg = (
    daily_df.groupby('season', observed=True)['total_count']
    .mean()
    .reset_index()
    .sort_values(by='total_count', ascending=False)
)
colors_s = ['#1f77b4' if x == season_avg['total_count'].max() else '#b0c4de' for x in season_avg['total_count']]
sns.barplot(data=season_avg, x='season', y='total_count', hue='season', palette=colors_s, legend=False, ax=axes1[0])
axes1[0].set_title("Rata-rata Penyewaan Harian berdasarkan Musim", fontweight='bold')
axes1[0].set_xlabel("Musim")
axes1[0].set_ylabel("Rata-rata Penyewaan (Unit)")
for container in axes1[0].containers:
    axes1[0].bar_label(container, fmt='%.0f', padding=3, fontweight='bold')

weather_avg = (
    daily_df.groupby('day_weathersit', observed=True)['total_count']
    .mean()
    .reset_index()
    .sort_values(by='total_count', ascending=False)
)
colors_w = ['#1f77b4' if x == weather_avg['total_count'].max() else '#b0c4de' for x in weather_avg['total_count']]
sns.barplot(data=weather_avg, x='day_weathersit', y='total_count', hue='day_weathersit', palette=colors_w, legend=False, ax=axes1[1])
axes1[1].set_title("Rata-rata Penyewaan Harian berdasarkan Kondisi Cuaca", fontweight='bold')
axes1[1].set_xlabel("Kondisi Cuaca")
axes1[1].set_ylabel("Rata-rata Penyewaan (Unit)")
for container in axes1[1].containers:
    axes1[1].bar_label(container, fmt='%.0f', padding=3, fontweight='bold')

plt.tight_layout()
st.pyplot(fig1)

st.divider()

# --- PERTANYAAN 2: POLA PENYEWAAN PER JAM ---
st.subheader("2. Pola Penyewaan per Jam: Pengguna Casual vs Registered")
hourly_pattern = filtered_df.groupby(['workingday', 'hour'], observed=True).agg(
    avg_casual=('casual', 'mean'),
    avg_registered=('registered', 'mean')
).reset_index()

available_day_types = hourly_pattern['workingday'].unique().tolist()
fig2, axes2 = plt.subplots(1, len(available_day_types), figsize=(15, 5.5), sharey=True)
if len(available_day_types) == 1:
    axes2 = [axes2]

for idx, day_type in enumerate(available_day_types):
    subset = hourly_pattern[hourly_pattern['workingday'] == day_type]
    axes2[idx].plot(subset['hour'], subset['avg_registered'], marker='o', linewidth=2.5, color='#1f77b4', label='Registered')
    axes2[idx].plot(subset['hour'], subset['avg_casual'], marker='s', linewidth=2.5, color='#ff7f0e', label='Casual')
    axes2[idx].set_title(f"Pola per Jam: {day_type}", fontweight='bold')
    axes2[idx].set_xlabel("Jam (00:00 - 23:00)")
    axes2[idx].set_xticks(range(0, 24))
    axes2[idx].grid(True, linestyle='--', alpha=0.6)
    axes2[idx].legend()

axes2[0].set_ylabel("Rata-rata Penyewaan per Jam (Unit)")
plt.tight_layout()
st.pyplot(fig2)

st.divider()

# --- PERTANYAAN 3: PERTUMBUHAN BULANAN Q4 (2011 VS 2012) ---
st.subheader("3. Evaluasi Kinerja & Pertumbuhan Bulanan (MoM %) Kuartal 4 (2011 vs 2012)")
st.caption("Catatan: Grafik di bawah menampilkan perbandingan penuh Q4 2011 vs Q4 2012 agar perhitungan persentase pertumbuhan bulanan (Month-over-Month) tetap akurat.")

monthly_all = df.groupby(['year', 'month'], observed=True)['total_count'].sum().reset_index()
monthly_all['MoM_growth_%'] = (monthly_all.groupby('year', observed=True)['total_count'].pct_change() * 100).round(2)
q4_df = monthly_all[monthly_all['month'].isin(['Oct', 'Nov', 'Dec'])].copy()
q4_df['month'] = q4_df['month'].cat.remove_unused_categories()
q4_df['year'] = q4_df['year'].astype(str)

fig3, axes3 = plt.subplots(1, 2, figsize=(15, 5.5))
sns.barplot(data=q4_df, x='month', y='total_count', hue='year', palette=['#a6bddb', '#1f77b4'], ax=axes3[0])
axes3[0].set_title("Total Volume Penyewaan Bulanan Q4 (2011 vs 2012)", fontweight='bold')
axes3[0].set_xlabel("Bulan (Q4)")
axes3[0].set_ylabel("Total Penyewaan (Unit)")
axes3[0].legend(title="Tahun")
for container in axes3[0].containers:
    axes3[0].bar_label(container, fmt='%.0f', padding=3, fontweight='bold')

sns.barplot(data=q4_df, x='month', y='MoM_growth_%', hue='year', palette=['#fc9272', '#de2d26'], ax=axes3[1])
axes3[1].axhline(0, color='black', linewidth=1)
axes3[1].set_title("Tingkat Pertumbuhan Bulanan (MoM %) pada Q4", fontweight='bold')
axes3[1].set_xlabel("Bulan (Q4)")
axes3[1].set_ylabel("Pertumbuhan MoM (%)")
axes3[1].legend(title="Tahun")
for container in axes3[1].containers:
    axes3[1].bar_label(container, fmt='%.1f%%', padding=3, fontweight='bold')

plt.tight_layout()
st.pyplot(fig3)

st.divider()

# --- ANALISIS LANJUTAN: KLASTER WAKTU OPERASIONAL ---
if 'time_cluster' in filtered_df.columns:
    st.subheader("4. Analisis Lanjutan: Rata-rata Penyewaan berdasarkan Klaster Waktu Operasional")
    cluster_df = filtered_df.groupby(['workingday', 'time_cluster'], observed=True)['total_count'].mean().reset_index()

    fig4, ax4 = plt.subplots(figsize=(12, 5))
    sns.barplot(data=cluster_df, x='time_cluster', y='total_count', hue='workingday', palette=['#ff7f0e', '#1f77b4'], ax=ax4)
    ax4.set_title("Rata-rata Penyewaan per Jam berdasarkan Klaster Waktu", fontweight='bold')
    ax4.set_xlabel("Klaster Waktu (Time-of-Day)")
    ax4.set_ylabel("Rata-rata Penyewaan per Jam (Unit)")
    ax4.legend(title="Tipe Hari")
    for container in ax4.containers:
        ax4.bar_label(container, fmt='%.1f', padding=3, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig4)