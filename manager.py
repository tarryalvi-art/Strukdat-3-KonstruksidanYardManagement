from stack import Stack
from yard_queue import Queue
 
 
class MaterialBlokirError(Exception):
    """Material di bawah tumpukan terhalang material lain di atasnya."""
 
 
class YardManager:
    """Pengelola utama: Stack (tumpukan), Queue (permintaan), Logger, Validator."""
 
    def __init__(self, kapasitas=None, logger=None, validator=None):
        self.stack = Stack(kapasitas)
        self.antrean = Queue()
        self.logger = logger
        self.validator = validator
 
    def _cek(self, nama):
        return self.validator.validasi_nama(nama) if self.validator else nama
 
    def _log(self, pesan):
        if self.logger:
            self.logger.catat(pesan)
 
    def tambah_material(self, nama):
        nama = self._cek(nama)
        self.stack.push(nama)
        self._log(f"PUSH: {nama}")
        return nama
 
    def ambil_material(self):
        nama = self.stack.pop()
        self._log(f"POP: {nama}")
        return nama
 
    def ajukan_permintaan(self, nama):
        nama = self._cek(nama)
        self.antrean.enqueue(nama)
        self._log(f"REQUEST: {nama}")
        return nama
 
    def proses_permintaan(self):
        """Proses permintaan terdepan. Jika gagal, permintaan tetap di antrean."""
        nama = self.antrean.peek()
        if nama not in self.stack:
            self._log(f"GAGAL: {nama} tidak tersedia")
            raise ValueError(f"Material '{nama}' tidak tersedia di tumpukan.")
        atas = self.stack.items_above(nama)
        if atas:
            self._log(f"DITOLAK: {nama} terblokir oleh {', '.join(atas)}")
            raise MaterialBlokirError(
                f"'{nama}' terblokir. Pindahkan dulu: {', '.join(atas)}."
            )
        self.stack.pop()
        self.antrean.dequeue()
        self._log(f"PROSES: {nama}")
        return nama
 
    def lihat_tumpukan(self):
        return list(self.stack)  # urut dari atas ke bawah
 
    def lihat_antrean(self):
        return list(self.antrean)  # urut dari depan ke belakang
 
