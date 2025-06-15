# CV Analyzer - Tubes 3 Strategi Algoritma

Aplikasi desktop untuk menganalisis CV menggunakan algoritma string matching yang berbeda. Aplikasi ini memungkinkan pencarian keyword dalam database CV dengan menggunakan algoritma KMP, Boyer-Moore, dan Fuzzy Search sebagai fallback.

## Algoritma yang Diimplementasikan

### 1. Knuth-Morris-Pratt (KMP)
Algoritma KMP adalah algoritma pencarian string yang efisien dengan kompleksitas waktu O(n+m), dimana n adalah panjang teks dan m adalah panjang pattern. KMP menggunakan fungsi failure untuk menghindari pergeseran yang tidak perlu ketika terjadi mismatch, sehingga tidak pernah mundur dalam teks yang sedang diperiksa.

**Keunggulan:**
- Tidak pernah mundur dalam teks (no backtracking)
- Kompleksitas waktu linear O(n+m)
- Efisien untuk pattern yang memiliki prefix yang berulang

### 2. Boyer-Moore (BM)
Algoritma Boyer-Moore adalah algoritma pencarian string yang menggunakan dua heuristik: bad character rule dan good suffix rule. Algoritma ini memulai pencocokan dari akhir pattern dan dapat melakukan skip yang besar ketika terjadi mismatch.

**Keunggulan:**
- Performa terbaik pada teks yang besar
- Dapat melakukan skip besar ketika mismatch
- Efektif untuk pattern yang panjang
- Kompleksitas rata-rata O(n/m) dalam kasus terbaik

### 3. Fuzzy Search (Levenshtein Distance)
Fuzzy search menggunakan Levenshtein Distance untuk menemukan string yang mirip ketika pencarian exact tidak menemukan hasil. Algoritma ini menghitung jumlah minimum operasi edit (insert, delete, substitute) yang diperlukan untuk mengubah satu string menjadi string lain.

**Fungsi:**
- Fallback ketika KMP/BM tidak menemukan hasil
- Toleran terhadap typo dan kesalahan pengetikan
- Menggunakan threshold similarity untuk menentukan kecocokan

## Requirements

### Sistem Requirements
- **Operating System:** Windows 10/11, macOS 10.14+, atau Linux Ubuntu 18.04+
- **Python:** 3.8 atau lebih baru
- **RAM:** Minimum 4GB (Recommended 8GB)
- **Storage:** Minimum 2GB free space

### Dependencies
- **PySide6** - untuk GUI framework
- **PyPDF2** atau **pdfplumber** - untuk ekstraksi teks dari PDF
- **mysql-connector-python** - untuk koneksi database MySQL
- **rapidfuzz** - untuk fuzzy string matching (opsional)

## Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/your-username/Tubes3_gurt-yo.git
cd Tubes3_gurt-yo
```

### 2. Setup Python Environment
```bash
# Buat virtual environment
python -m venv env

# Aktivasi virtual environment
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Start MySQL server
mysql -u root -p

# Buat database
CREATE DATABASE cv_analyzer;
```

### 5. Konfigurasi Database
```bash
# Copy file konfigurasi
cp config/database.example.json config/database.json

# Edit config/database.json dengan kredensial MySQL Anda
{
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "port": 3306,
    "database": "cv_analyzer"
}
```

## Cara Penggunaan

### 1. Persiapan Data CV
- Download dataset CV dari [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
- Ekstrak file dan tempatkan di folder `data/`
- Struktur folder: `data/JOB_CATEGORY/cv_files.pdf`

### 2. Seed Database
```bash
make test-seeder
```

### 3. Menjalankan Aplikasi
```bash
make run
```

### 4. Menggunakan Aplikasi
1. **Load Database:** Klik "Load Database" untuk menghubungkan ke database
2. **Input Keywords:** Masukkan keyword yang ingin dicari (pisahkan dengan koma)
3. **Pilih Algoritma:** Pilih KMP atau Boyer-Moore
4. **Set Top Matches:** Tentukan jumlah hasil teratas yang ingin ditampilkan
5. **Search:** Klik "Search CVs" untuk memulai pencarian
6. **View Results:** Lihat hasil pencarian dengan informasi:
   - Exact Match: menggunakan KMP/BM
   - Fuzzy Match: menggunakan Levenshtein Distance (fallback)

## Testing

### Test PDF Extraction
```bash
make test-extract-1
```

### Test Database Seeder
```bash
make test-seeder
```

### Test Search Algorithms
```bash
make test-search
```

## Struktur Project
```
Tubes3_gurt-yo/
├── src/                    # Source code utama
│   ├── main.py            # File utama aplikasi
│   ├── Search/            # Implementasi algoritma pencarian
│   │   ├── KMP.py         # Algoritma KMP
│   │   ├── BM.py          # Algoritma Boyer-Moore
│   │   └── Fuzzy.py       # Algoritma Fuzzy Search
│   ├── ExtractCV.py       # Ekstraksi teks dari PDF
│   ├── Database.py        # Koneksi dan operasi database
│   └── SearchWorker.py    # Threading untuk pencarian
├── test/                  # File testing
├── config/                # Konfigurasi database
├── data/                  # Dataset CV (tidak di-track git)
├── requirements.txt       # Dependencies Python
└── Makefile              # Automation commands
```

## Fitur Utama

### 🔍 **Multi-Algorithm Search**
- KMP untuk exact matching yang efisien
- Boyer-Moore untuk performa optimal pada teks besar
- Fuzzy search sebagai fallback untuk typo tolerance

### ⚡ **Performance Tracking**
- Waktu eksekusi terpisah untuk exact dan fuzzy search
- Jumlah CV yang di-scan untuk setiap algoritma
- Statistik performa real-time

### 🎨 **User-Friendly Interface**
- GUI modern dengan PySide6
- Loading animation dengan progress tracking
- Real-time search progress
- Hasil pencarian dengan format card yang informatif

### 🗄️ **Database Integration**
- MySQL database untuk menyimpan metadata CV
- Dynamic database configuration
- Efficient CV data retrieval

## Troubleshooting

### Error: "QLayout: Attempting to add QLayout"
- Pastikan tidak ada duplikasi layout creation
- Restart aplikasi

### Error: "Database connection failed"
- Periksa kredensial di `config/database.json`
- Pastikan MySQL server berjalan
- Pastikan database sudah dibuat

### Error: "ModuleNotFoundError"
- Jalankan `pip install -r requirements.txt`
- Pastikan virtual environment sudah diaktivasi

## Author

**Tim Gurt:Yo - Kelompok X**

| NIM | Nama | Role |
|-----|------|------|
| 13523032 | Nathan Jovial Hartono |
| 13523070 | Sebastian Hung Yansen |
| 13523093 | Karol Yangqian Poetracahya |

**Mata Kuliah:** IF2211 Strategi Algoritma  
**Semester:** 4  
**Tahun Akademik:** 2024/2025  
**Institut Teknologi Bandung**