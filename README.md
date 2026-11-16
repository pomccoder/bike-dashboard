# Proyek Analisis Data: Bike Sharing Dataset 🚲

Proyek ini merupakan hasil analisis data eksploratif dan pembuatan dashboard interaktif menggunakan dataset **Capital Bikeshare (2011–2012)** di Washington D.C. Analisis difokuskan pada pengaruh kondisi cuaca dan musim terhadap permintaan penyewaan sepeda harian, perbedaan pola penyewaan per jam antara pengguna kasual (*casual*) dan terdaftar (*registered*), serta evaluasi pertumbuhan bulanan pada Kuartal 4.

## 📁 Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## ⚙️ Panduan Instalasi & Menjalankan Dashboard

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan kerja (*environment*) dan menjalankan dashboard Streamlit secara lokal:

### 1. Membuat Virtual Environment
Buka terminal pada direktori utama proyek (`submission/`), lalu buat *virtual environment* baru dengan perintah:
```bash
python -m venv .venv
```

### 2. Mengaktifkan Virtual Environment
Aktifkan *virtual environment* sesuai dengan jenis terminal dan sistem operasi yang Anda gunakan:

- **Command Prompt (CMD - Windows):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **PowerShell (Windows):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Menginstal Library yang Dibutuhkan
Pastikan *virtual environment* sudah aktif (ditandai dengan munculnya `(.venv)` di awal baris terminal), lalu instal seluruh *library* yang tercantum di dalam `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard Streamlit
Jalankan aplikasi dashboard utama (`dashboard/dashboard.py`) menggunakan perintah berikut:
```bash
streamlit run dashboard/dashboard.py
```

Setelah perintah dijalankan, aplikasi akan otomatis terbuka di browser default Anda pada alamat lokal (umumnya `http://localhost:8501`).

## 🌐 Akses Dashboard Online (Streamlit Cloud)
Tautan menuju dashboard yang telah di-*deploy* secara online juga tersedia pada berkas `url.txt` di dalam direktori utama proyek ini.
