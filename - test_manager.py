import os
import sys
import unittest
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
 
from logger import Logger
from manager import YardManager, MaterialBlokirError
from validator import MaterialValidator
from stack import StackEmptyError, StackFullError
from yard_queue import QueueEmptyError
 
 
class TestYardManager(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.m = YardManager(logger=self.log, validator=MaterialValidator)
 
    def kategori(self):
        return [e[1] for e in self.log.get_entries()]
 
    def isi(self):
        self.m.tambah_material("BJ-01", "Baja", 10)
        self.m.tambah_material("BJ-02", "Kontainer", 20)
        self.m.tambah_material("BJ-03", "Pipa", 5)
 
    def test_tambah_dan_ambil_lifo(self):
        self.isi()
        self.assertEqual(self.m.lihat_tumpukan(), ["BJ-03", "BJ-02", "BJ-01"])
        self.assertEqual(self.m.ambil_material().kode, "BJ-03")
        self.assertEqual(self.kategori(), ["PUSH"] * 3 + ["POP"])
 
    def test_ambil_kosong_dan_overflow(self):
        with self.assertRaises(StackEmptyError):
            self.m.ambil_material()
        kecil = YardManager(kapasitas=1, logger=self.log)
        kecil.tambah_material("A", "a", 1)
        with self.assertRaises(StackFullError):
            kecil.tambah_material("B", "b", 1)
        self.assertEqual(self.kategori().count("ERROR"), 2)
 
    def test_validator_menolak_input_salah(self):
        with self.assertRaises(ValueError):
            self.m.tambah_material("", "Baja", 10)
        with self.assertRaises(ValueError):
            self.m.ajukan_permintaan("")
        self.assertEqual(self.m.lihat_tumpukan(), [])
        self.assertEqual(self.m.lihat_antrean(), [])
 
    def test_proses_permintaan_fifo(self):
        self.isi()
        self.m.ajukan_permintaan("BJ-03")
        self.m.ajukan_permintaan("BJ-02")
        self.assertEqual(self.m.proses_permintaan(), "BJ-03")
        self.assertEqual(self.m.proses_permintaan(), "BJ-02")
        self.assertEqual(self.m.lihat_tumpukan(), ["BJ-01"])
        self.assertEqual(self.kategori()[-2:], ["PROCESS", "PROCESS"])
 
    def test_material_terblokir(self):
        self.isi()
        self.m.ajukan_permintaan("BJ-01")
        with self.assertRaises(MaterialBlokirError) as e:
            self.m.proses_permintaan()
        self.assertIn("BJ-03", str(e.exception))
        self.assertIn("BJ-02", str(e.exception))
        self.assertIn("BLOCKED", self.kategori())
        self.assertEqual(self.m.lihat_antrean(), ["BJ-01"])
        self.assertEqual(len(self.m.lihat_tumpukan()), 3)
        self.m.ambil_material()
        self.m.ambil_material()
        self.assertEqual(self.m.proses_permintaan(), "BJ-01")
 
    def test_material_tidak_tersedia(self):
        self.m.ajukan_permintaan("XX-99")
        with self.assertRaises(ValueError):
            self.m.proses_permintaan()
        self.assertEqual(self.m.lihat_antrean(), ["XX-99"])
 
    def test_antrean_kosong(self):
        with self.assertRaises(QueueEmptyError):
            self.m.proses_permintaan()
 
 
if __name__ == "__main__":
    unittest.main()
 
