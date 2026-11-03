# Hasil Pengujian Integrasi

Dokumen ini berisi bukti pengujian seluruh komponen yang digabungkan: `Node`, `Stack`,
`Queue`, `Logger`, `Validator`, `YardManager`, dan `main.py`.

## 1. Lingkungan
- Python: `3.x` *(isi sesuai hasil `python --version` di laptop)*
- Sistem operasi: *(isi, misal Windows 11)*
- Dijalankan dari folder utama repository, branch `main`

## 2. Pengujian Otomatis (unit test dan integrasi)
Perintah:
```bash
python -m unittest discover -s src -p "test_*.py" -v
```

Hasil: *(tempel keluaran terminal di bawah ini, atau ganti dengan screenshot)*
```text
...
Ran N tests in 0.0XXs

OK
```

| Modul | File test | Yang diuji |
|---|---|---|
| Node dan Stack | `test_stack.py` | LIFO, underflow, overflow, `items_above` |
| Queue | `test_queue.py` | FIFO, antrean kosong, overflow |
| Logger | `test_logger.py` | Pencatatan semua kategori, urutan, tampilan riwayat |
| Validator | `test_validator.py` | Kode, nama, dan berat valid dan tidak valid |
| YardManager | `test_manager.py` | Tambah, ambil, ajukan, proses, material terblokir |
| Integrasi | `test_integration.py` | Semua modul bisa diimpor, alur menu lengkap, input salah |

## 3. Skenario Pengujian Manual (`python src/main.py`)
Kapasitas tumpukan: 10 material.

### Skenario 1: Alur normal dan material terblokir
Tujuan: permintaan material di bawah tumpukan harus ditolak, lalu berhasil setelah penghalangnya diambil.

```text
Pilih menu: 1   (BJ-01, Baja, 10)  -> Berhasil menumpuk BJ-01 'Baja'.
Pilih menu: 1   (BJ-02, Pipa, 5)   -> Berhasil menumpuk BJ-02 'Pipa'.
Pilih menu: 5   -> Tumpukan (atas -> bawah): ['BJ-02', 'BJ-01']
Pilih menu: 3   (BJ-01)            -> Permintaan diajukan: BJ-01
Pilih menu: 6   -> Antrean (depan -> belakang): ['BJ-01']
Pilih menu: 4   -> [!] 'BJ-01' terblokir. Pindahkan dulu: BJ-02 'Pipa'.
Pilih menu: 2   -> Diambil: BJ-02 'Pipa'
Pilih menu: 4   -> Permintaan diproses, material BJ-01 keluar.
Pilih menu: 5   -> Tumpukan (atas -> bawah): kosong
```
Hasil: sesuai harapan. LIFO terbukti (BJ-02 harus keluar lebih dulu), dan permintaan yang ditolak tetap di antrean.

### Skenario 2: Overflow (tumpukan penuh)
Tujuan: menambah material ke-11 harus ditolak.
```text
Pilih menu: 1   (K-10, Baja, 1)  -> Berhasil menumpuk K-10 'Baja'.
Pilih menu: 1   (K-11, Baja, 1)  -> [!] Stack penuh (kapasitas 10).
```
Hasil: sesuai harapan, program tidak berhenti.

### Skenario 3: Input salah
| Input | Hasil |
|---|---|
| Menu `9` | `[!] Menu tidak valid.` |
| Berat `abc` | `[!] Berat harus berupa angka.` |
| Kode dikosongkan | `[!] Kode material tidak boleh kosong dan harus berupa teks.` |
| Berat `-5` | `[!] Berat material harus angka lebih besar dari 0.` |

Hasil: semua ditolak dengan pesan jelas, program tetap berjalan.

### Skenario 4: Underflow dan permintaan tidak valid
| Kondisi | Hasil |
|---|---|
| Ambil material dari tumpukan kosong (menu 2) | `[!] Stack kosong, tidak bisa pop.` |
| Proses permintaan saat antrean kosong (menu 4) | `[!] Antrean kosong, tidak bisa peek.` |
| Minta material yang tidak ada (`XX-99`), lalu proses | `[!] Material 'XX-99' tidak tersedia di tumpukan.` |

Hasil: sesuai harapan.

### Skenario 5: Riwayat aktivitas
Menu 7 menampilkan catatan berurutan dengan kategori PUSH, POP, REQUEST, PROCESS, BLOCKED,
dan ERROR sesuai aksi di atas. Urutan kategori diverifikasi otomatis di `test_integration.py`.

## 4. Kesimpulan
Semua komponen terhubung dan berjalan sesuai spesifikasi: tumpukan LIFO, antrean FIFO,
validasi akses terblokir, log bongkar-muat, serta penanganan underflow, overflow, dan input salah.