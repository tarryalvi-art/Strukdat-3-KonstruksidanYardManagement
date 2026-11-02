import importlib
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
 
import main
from logger import Logger
from manager import YardManager, MaterialBlokirError
from validator import MaterialValidator
 
 
def jalankan_menu(*masukan):
    """Jalankan main() dengan input tiruan, kembalikan seluruh keluarannya."""
    buf = io.StringIO()
    with patch("builtins.input", side_effect=list(masukan)), redirect_stdout(buf):
        main.main()
    return buf.getvalue()
 
 
class TestIntegrasi(unittest.TestCase):
    def test_semua_modul_bisa_diimpor(self):
        for nama in ["node", "stack", "yard_queue", "logger", "validator", "manager", "main"]:
            importlib.import_module(nama)
 
    def test_alur_lengkap_komponen(self):
        log = Logger()
        m = YardManager(3, log, MaterialValidator)
        m.tambah_material("BJ-01", "Baja", 10)
        m.tambah_material("BJ-02", "Kontainer", 20)
        m.ajukan_permintaan("BJ-01")
        with self.assertRaises(MaterialBlokirError):
            m.proses_permintaan()
        m.ambil_material()
        self.assertEqual(m.proses_permintaan(), "BJ-01")
        kategori = [e[1] for e in log.get_entries()]
        self.assertEqual(kategori, ["PUSH", "PUSH", "REQUEST", "BLOCKED", "POP", "PROCESS"])
 
    def test_menu_alur_normal_dan_blokir(self):
        out = jalankan_menu(
            "1", "BJ-01", "Baja", "10",
            "1", "BJ-02", "Pipa", "5",
            "3", "BJ-01",
            "4",            # terblokir oleh BJ-02
            "2",            # ambil BJ-02
            "4",            # BJ-01 berhasil
            "7", "0",
        )
        self.assertIn("terblokir", out)
        self.assertIn("Pindahkan dulu", out)
        self.assertIn("Permintaan diproses, material BJ-01 keluar", out)
        self.assertIn("RIWAYAT AKTIVITAS", out)
 
    def test_menu_input_salah_tidak_crash(self):
        out = jalankan_menu(
            "9",                          # menu tidak ada
            "1", "BJ-01", "Baja", "abc",  # berat bukan angka
            "1", "", "Baja", "10",        # kode kosong
            "2",                          # ambil dari tumpukan kosong
            "4",                          # proses antrean kosong
            "0",
        )
        self.assertIn("Menu tidak valid", out)
        self.assertIn("Berat harus berupa angka", out)
        self.assertIn("Kode material tidak boleh kosong", out)
        self.assertIn("Stack kosong", out)
        self.assertIn("Antrean kosong", out)
        self.assertIn("Terima kasih", out)
 
    def test_overflow_lewat_menu(self):
        masuk = []
        for i in range(main.KAPASITAS + 1):
            masuk += ["1", f"K-{i}", "Baja", "1"]
        out = jalankan_menu(*masuk, "0")
        self.assertIn("Stack penuh", out)
 
 
if __name__ == "__main__":
    unittest.main()
 