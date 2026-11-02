# Yard Management System
### Konstruksi dan Manajemen Tumpukan Material

Proyek kelompok **Struktur Data dan Algoritma — Kelompok 3**.

Yard Management System adalah aplikasi berbasis **Command-Line Interface (CLI)** yang digunakan untuk mengelola tumpukan material berat di area penyimpanan terbatas. Program ini menerapkan struktur data **Stack (LIFO)** dan **Queue (FIFO)** yang diimplementasikan secara mandiri menggunakan *linked list*.

Implementasi Stack dan Queue dibuat tanpa menggunakan `queue.Queue` maupun `list.pop(0)` untuk memenuhi ketentuan proyek.

## Fitur Utama

### 1. Manajemen Tumpukan Material (Stack)
- Menambahkan material menggunakan operasi `push()`.
- Mengambil material paling atas menggunakan operasi `pop()`.
- Melihat material paling atas menggunakan operasi `peek()`.
- Menerapkan prinsip **LIFO (*Last In, First Out*)**.
- Membatasi jumlah material berdasarkan kapasitas tumpukan.

### 2. Manajemen Antrean Permintaan (Queue)
- Mengajukan permintaan material ke dalam antrean.
- Memproses permintaan berdasarkan urutan kedatangan.
- Menerapkan prinsip **FIFO (*First In, First Out*)**.
- Mengelola antrean menggunakan *linked list*.

### 3. Validasi Akses Material
- Memeriksa ketersediaan material berdasarkan kode.
- Menolak pengambilan material yang masih tertutup oleh material lain di atasnya.
- Menampilkan daftar material yang harus dipindahkan terlebih dahulu sebelum material yang diminta dapat diambil.

### 4. Pencatatan Aktivitas (Logger)
Mencatat aktivitas sistem, meliputi:
- Penambahan material.
- Pengambilan material.
- Pengajuan dan pemrosesan permintaan.
- Penolakan permintaan.
- Kesalahan yang terjadi selama program berjalan.

### 5. Validasi Input dan Penanganan Error
- Memvalidasi data material dan permintaan.
- Menangani kondisi *underflow* ketika Stack kosong.
- Menangani kondisi *overflow* ketika kapasitas Stack penuh.
- Menangani input yang tidak valid tanpa langsung menghentikan program.

## Struktur Folder

```text
yard-management/
├── src/
│   ├── node.py
│   ├── stack.py
│   ├── yard_queue.py
│   ├── logger.py
│   ├── validator.py
│   ├── manager.py
│   ├── main.py
│   ├── test_stack.py
│   ├── test_queue.py
│   ├── test_logger.py
│   ├── test_validator.py
│   ├── test_manager.py
│   └── test_integration.py
├── README.md
└── .gitignore
```

### Deskripsi File

| File | Fungsi |
|---|---|
| `node.py` | Mendefinisikan node untuk struktur data berbasis *linked list*. |
| `stack.py` | Mengimplementasikan Stack dengan prinsip LIFO. |
| `yard_queue.py` | Mengimplementasikan Queue dengan prinsip FIFO. |
| `logger.py` | Mencatat dan menampilkan riwayat aktivitas program. |
| `validator.py` | Memvalidasi data material dan permintaan. |
| `manager.py` | Menghubungkan Stack, Queue, Logger, dan Validator melalui class `YardManager`. |
| `main.py` | Menjalankan program utama melalui menu CLI. |
| `test_stack.py` | Menguji fungsi dan perilaku Stack. |
| `test_queue.py` | Menguji fungsi dan perilaku Queue. |
| `test_logger.py` | Menguji pencatatan aktivitas. |
| `test_validator.py` | Menguji validasi data dan penanganan input. |
| `test_manager.py` | Menguji fungsi dan interaksi `YardManager`. |
| `test_integration.py` | Menguji integrasi antarkomponen sistem. |

## Persyaratan Sistem

- Python versi **3.8 atau lebih baru**.
- Terminal atau Command Prompt.
- Tidak memerlukan pustaka eksternal jika seluruh implementasi menggunakan modul bawaan Python.

## Cara Menjalankan Program

1. Pastikan Python sudah terinstal.
2. Buka terminal pada direktori utama proyek.
3. Jalankan perintah berikut:

```bash
python src/main.py
```

4. Ikuti petunjuk menu yang ditampilkan untuk menggunakan fitur manajemen material.

### Format Data Material

Data material menggunakan informasi berikut:

| Atribut | Contoh | Keterangan |
|---|---|---|
| Kode material | `BJ-01` | Identitas unik material. |
| Nama material | `Baja H-Beam` | Nama atau jenis material. |
| Berat | `2.5` ton | Berat material dalam satuan ton. |

Format tersebut merupakan contoh data. Ketentuan input yang sebenarnya mengikuti implementasi program.

## Menjalankan Pengujian

Pengujian dilakukan menggunakan modul `unittest` bawaan Python.

Untuk menjalankan seluruh pengujian yang sesuai dengan pola nama `test_*.py` di dalam folder `src/`, gunakan perintah:

```bash
python -m unittest discover -s src -p "test_*.py" -v
```

Perintah tersebut akan menemukan dan menjalankan pengujian modul yang sesuai dengan pola nama file tersebut.

Opsi `-v` (*verbose*) menampilkan nama setiap pengujian beserta hasilnya.

## Aturan Kolaborasi GitHub

Pengembangan proyek dilakukan secara kolaboratif menggunakan GitHub dengan ketentuan berikut:

1. Setiap anggota mengerjakan tugas pada branch fitur masing-masing.
2. Setiap anggota melakukan *commit* terhadap perubahan yang dibuat.
3. Setelah pekerjaan selesai, anggota mengajukan **Pull Request (PR)**.
4. Perubahan diperiksa sebelum digabungkan ke branch `main`.
5. Setiap anggota bertanggung jawab menguji modul yang dikerjakannya.
6. Integrasi akhir dilakukan untuk memastikan seluruh modul dapat bekerja bersama.

### Format Commit

Gunakan format berikut:

```text
jenis: deskripsi singkat
```

Contoh:

```text
feat: add stack implementation
fix: handle empty queue error
test: add stack unit tests
docs: update project readme
refactor: improve material validation
chore: organize project files
```

Jenis commit yang digunakan:

| Jenis | Kegunaan |
|---|---|
| `feat` | Menambahkan fitur baru. |
| `fix` | Memperbaiki kesalahan program. |
| `test` | Menambahkan atau memperbaiki pengujian. |
| `docs` | Mengubah dokumentasi. |
| `refactor` | Merapikan kode tanpa mengubah fungsi utamanya. |
| `chore` | Melakukan pemeliharaan atau pengaturan proyek. |

## Pembagian Tugas Anggota

| Anggota | Tanggung Jawab | Branch |
|---|---|---|
| Anggota 1 | Node dan Stack | `feature/node-stack` |
| Anggota 2 | Queue dan Pengujian Antrean | `feature/queue` |
| Anggota 3 | YardManager | `feature/yard-manager` |
| Anggota 4 | Logger dan Riwayat Aktivitas | `feature/logger` |
| Anggota 5 | Validasi Data dan Penanganan Error | `feature/validator` |
| Anggota 6 | Program Utama, Integrasi, GitHub, dan Dokumentasi | `feature/main-integration` |

## Tujuan Akhir Proyek

Proyek ini bertujuan menerapkan konsep struktur data dan algoritma melalui aplikasi pengelolaan material yang modular, teruji, dan mudah digunakan. Penerapan Stack, Queue, *linked list*, validasi data, pencatatan aktivitas, serta kolaborasi GitHub diharapkan menghasilkan program yang terstruktur dan sesuai dengan spesifikasi tugas.

---

**Kelompok 3 — Proyek Struktur Data dan Algoritma**