import os
import sys
import unittest
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
 
from manager import YardManager, MaterialBlokirError
from stack import StackEmptyError, StackFullError
from yard_queue import QueueEmptyError
 
 
class FakeLogger:
    def __init__(self):
        self.pesan = []
 
    def catat(self, pesan):
        self.pesan.append(pesan)
 
 
class FakeValidator:
    def validasi_nama(self, nama):
        if not nama or not nama.strip():
            raise ValueError("Nama material tidak boleh kosong.")
        return nama.strip()
 
 
class TestYardManager(unittest.TestCase):
    def setUp(self):
        self.log = FakeLogger()
        self.m = YardManager(logger=self.log, validator=FakeValidator())
 
    def test_tambah_dan_ambil_lifo(self):
        self.m.tambah_material("Baja")
        self.m.tambah_material("Pipa")
        self.assertEqual(self.m.lihat_tumpukan(), ["Pipa", "Baja"])
        self.assertEqual(self.m.ambil_material(), "Pipa")
        self.assertEqual(self.log.pesan, ["PUSH: Baja", "PUSH: Pipa", "POP: Pipa"])
 
    def test_ambil_kosong_dan_overflow(self):
        with self.assertRaises(StackEmptyError):
            self.m.ambil_material()
        kecil = YardManager(kapasitas=1)
        kecil.tambah_material("A")
        with self.assertRaises(StackFullError):
            kecil.tambah_material("B")
 
    def test_validator_menolak_input_salah(self):
        with self.assertRaises(ValueError):
            self.m.tambah_material("  ")
        with self.assertRaises(ValueError):
            self.m.ajukan_permintaan("")
        self.assertEqual(self.m.lihat_tumpukan(), [])
        self.assertEqual(self.m.lihat_antrean(), [])
 
    def test_proses_permintaan_fifo(self):
        self.m.tambah_material("Baja")
        self.m.tambah_material("Pipa")
        self.m.ajukan_permintaan("Pipa")
        self.m.ajukan_permintaan("Baja")
        self.assertEqual(self.m.proses_permintaan(), "Pipa")
        self.assertEqual(self.m.proses_permintaan(), "Baja")
        self.assertEqual(self.m.lihat_tumpukan(), [])
 
    def test_material_terblokir(self):
        for x in ["Baja", "Kontainer", "Pipa"]:
            self.m.tambah_material(x)
        self.m.ajukan_permintaan("Baja")
        with self.assertRaises(MaterialBlokirError) as e:
            self.m.proses_permintaan()
        self.assertIn("Pipa, Kontainer", str(e.exception))
        self.assertEqual(self.m.lihat_antrean(), ["Baja"])  # tetap di antrean
        self.assertEqual(len(self.m.lihat_tumpukan()), 3)   # stack tidak berubah
        self.m.ambil_material()
        self.m.ambil_material()
        self.assertEqual(self.m.proses_permintaan(), "Baja")
 
    def test_material_tidak_tersedia(self):
        self.m.ajukan_permintaan("Beton")
        with self.assertRaises(ValueError):
            self.m.proses_permintaan()
        self.assertEqual(self.m.lihat_antrean(), ["Beton"])
 
    def test_antrean_kosong(self):
        with self.assertRaises(QueueEmptyError):
            self.m.proses_permintaan()
 
 
if __name__ == "__main__":
    unittest.main()
 
