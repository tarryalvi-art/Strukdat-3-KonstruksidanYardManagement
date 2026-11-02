"""
logger.py
Pencatat riwayat aktivitas bongkar-muat pada sistem Yard Management.

Riwayat disimpan dalam linked list kustom (LogNode) agar konsisten dengan
aturan tugas (tanpa pustaka struktur data bawaan). Penambahan catatan di
akhir riwayat berjalan O(1) karena Logger menyimpan pointer tail.

Format satu baris log:
    [2026-10-26 10:15:30] PUSH     | Material BJ-01 'Baja H-Beam' (12.5 ton) ditumpuk

Cara pakai oleh YardManager:
    logger.catat_push(kode, nama, berat)
    logger.catat_pop(kode, nama)
    logger.catat_permintaan(kode)
    logger.catat_proses(kode)
    logger.catat_blocked(kode, jumlah_penghalang)
    logger.catat_error(pesan)
"""
from datetime import datetime


class LogNode:
    """Satu catatan aktivitas (node pada linked list riwayat)."""

    def __init__(self, waktu, kategori, pesan):
        self.waktu = waktu
        self.kategori = kategori
        self.pesan = pesan
        self.next = None


class Logger:
    """Mencatat dan menampilkan riwayat aktivitas program."""

    KATEGORI = ("PUSH", "POP", "REQUEST", "PROCESS", "BLOCKED", "ERROR", "INFO")

    def __init__(self):
        self._head = None
        self._tail = None
        self._jumlah = 0

    # ------------------------------------------------------------ pencatatan
    def log(self, kategori, pesan):
        """Tambahkan satu catatan generik ke akhir riwayat."""
        kategori = str(kategori).upper()
        if kategori not in self.KATEGORI:
            raise ValueError(
                f"Kategori log tidak dikenal: {kategori}. "
                f"Pilihan: {', '.join(self.KATEGORI)}"
            )
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node = LogNode(waktu, kategori, str(pesan))
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._jumlah += 1

    # Metode khusus per aktivitas: format pesan seragam di satu tempat.
    def catat_push(self, kode, nama, berat):
        self.log("PUSH", f"Material {kode} '{nama}' ({berat} ton) ditumpuk")

    def catat_pop(self, kode, nama):
        self.log("POP", f"Material {kode} '{nama}' diambil dari tumpukan")

    def catat_permintaan(self, kode):
        self.log("REQUEST", f"Permintaan material {kode} diajukan")

    def catat_proses(self, kode):
        self.log("PROCESS", f"Permintaan material {kode} berhasil diproses")

    def catat_blocked(self, kode, jumlah_penghalang):
        self.log(
            "BLOCKED",
            f"Material {kode} terblokir oleh {jumlah_penghalang} material di atasnya",
        )

    def catat_error(self, pesan):
        self.log("ERROR", pesan)

    # ------------------------------------------------------------ pembacaan
    def is_empty(self):
        return self._jumlah == 0

    def __len__(self):
        return self._jumlah

    def get_entries(self, kategori=None):
        """Kembalikan list tuple (waktu, kategori, pesan), terlama -> terbaru.
        Bisa difilter per kategori."""
        if kategori is not None:
            kategori = str(kategori).upper()
        hasil = []
        saat_ini = self._head
        while saat_ini is not None:
            if kategori is None or saat_ini.kategori == kategori:
                hasil.append((saat_ini.waktu, saat_ini.kategori, saat_ini.pesan))
            saat_ini = saat_ini.next
        return hasil

    @staticmethod
    def format_entri(waktu, kategori, pesan):
        """Susun satu baris log yang mudah dibaca."""
        return f"[{waktu}] {kategori:<8} | {pesan}"

    def show_history(self, limit=None, kategori=None):
        """Cetak riwayat aktivitas. limit = tampilkan N catatan terakhir."""
        entri = self.get_entries(kategori)
        print("\n" + "=" * 70)
        print("RIWAYAT AKTIVITAS BONGKAR-MUAT")
        print("=" * 70)
        if not entri:
            print("Belum ada aktivitas yang tercatat.")
            print("=" * 70)
            return
        if limit is not None and limit > 0:
            entri = entri[-limit:]
        for nomor, (waktu, kat, pesan) in enumerate(entri, start=1):
            print(f"{nomor:>3}. {self.format_entri(waktu, kat, pesan)}")
        print("=" * 70)
        print(f"Total ditampilkan: {len(entri)} dari {self._jumlah} catatan")