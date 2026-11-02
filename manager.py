from stack import Stack
from yard_queue import Queue
 
 
class MaterialBlokirError(Exception):
    """Material di bawah tumpukan terhalang material lain di atasnya."""
 
 
class Material:
    def __init__(self, kode, nama, berat):
        self.kode, self.nama, self.berat = kode, nama, berat
 
    def __eq__(self, other):  # dibandingkan lewat kode (Material atau str)
        return self.kode == getattr(other, "kode", other)
 
    def __repr__(self):
        return f"{self.kode} '{self.nama}'"
 
 
class YardManager:
    """Pengelola utama: Stack (tumpukan), Queue (permintaan), Logger, Validator."""
 
    def __init__(self, kapasitas=None, logger=None, validator=None):
        self.stack = Stack(kapasitas)
        self.antrean = Queue()
        self.logger = logger
        self.validator = validator
 
    def _log(self, metode, *args):
        if self.logger is not None:
            getattr(self.logger, metode)(*args)
 
    def _coba(self, fungsi, *args):
        """Jalankan fungsi; jika error, catat ke log lalu lempar ulang."""
        try:
            return fungsi(*args)
        except Exception as e:
            self._log("catat_error", str(e))
            raise
 
    def tambah_material(self, kode, nama, berat):
        if self.validator is not None:
            self._coba(self.validator.validasi_material, kode, nama, berat)
        m = Material(kode, nama, berat)
        self._coba(self.stack.push, m)
        self._log("catat_push", kode, nama, berat)
        return m
 
    def ambil_material(self):
        m = self._coba(self.stack.pop)
        self._log("catat_pop", m.kode, m.nama)
        return m
 
    def ajukan_permintaan(self, kode):
        if self.validator is not None:
            self._coba(self.validator.validasi_permintaan, kode)
        self._coba(self.antrean.enqueue, kode)
        self._log("catat_permintaan", kode)
        return kode
 
    def proses_permintaan(self):
        """Proses permintaan terdepan. Jika gagal, permintaan tetap di antrean."""
        kode = self._coba(self.antrean.peek)
        if kode not in self.stack:
            self._log("catat_error", f"Material {kode} tidak tersedia")
            raise ValueError(f"Material '{kode}' tidak tersedia di tumpukan.")
        atas = self.stack.items_above(kode)
        if atas:
            self._log("catat_blocked", kode, len(atas))
            raise MaterialBlokirError(
                f"'{kode}' terblokir. Pindahkan dulu: {', '.join(map(repr, atas))}."
            )
        self.stack.pop()
        self.antrean.dequeue()
        self._log("catat_proses", kode)
        return kode
 
    def lihat_tumpukan(self):
        return [m.kode for m in self.stack]  # atas -> bawah
 
    def lihat_antrean(self):
        return list(self.antrean)  # depan -> belakang
 
