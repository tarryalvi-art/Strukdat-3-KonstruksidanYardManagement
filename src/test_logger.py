"""Pengujian Logger. Jalankan: python -m unittest test_logger -v"""
import io
import re
import unittest
from contextlib import redirect_stdout

from logger import Logger

POLA_WAKTU = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


def tangkap_riwayat(logger, **kwargs):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        logger.show_history(**kwargs)
    return buffer.getvalue()


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    def test_awal_kosong(self):
        self.assertTrue(self.logger.is_empty())
        self.assertEqual(len(self.logger), 0)
        self.assertEqual(self.logger.get_entries(), [])

    def test_log_menambah_catatan(self):
        self.logger.log("INFO", "Sistem dimulai")
        self.assertEqual(len(self.logger), 1)
        self.assertFalse(self.logger.is_empty())

    def test_kategori_huruf_kecil_diterima(self):
        self.logger.log("push", "tes")
        self.assertEqual(self.logger.get_entries()[0][1], "PUSH")

    def test_kategori_tidak_dikenal_ditolak(self):
        with self.assertRaises(ValueError):
            self.logger.log("HAPUS", "tes")
        self.assertEqual(len(self.logger), 0)

    def test_urutan_terlama_ke_terbaru(self):
        for i in range(5):
            self.logger.log("INFO", f"pesan {i}")
        pesan = [e[2] for e in self.logger.get_entries()]
        self.assertEqual(pesan, [f"pesan {i}" for i in range(5)])

    def test_catat_push(self):
        self.logger.catat_push("BJ-01", "Baja H-Beam", 12.5)
        waktu, kat, pesan = self.logger.get_entries()[0]
        self.assertEqual(kat, "PUSH")
        self.assertIn("BJ-01", pesan)
        self.assertIn("Baja H-Beam", pesan)
        self.assertIn("12.5", pesan)
        self.assertRegex(waktu, POLA_WAKTU)

    def test_catat_pop(self):
        self.logger.catat_pop("BJ-02", "Kontainer A")
        _, kat, pesan = self.logger.get_entries()[0]
        self.assertEqual(kat, "POP")
        self.assertIn("BJ-02", pesan)

    def test_catat_permintaan_dan_proses(self):
        self.logger.catat_permintaan("BJ-01")
        self.logger.catat_proses("BJ-01")
        kategori = [e[1] for e in self.logger.get_entries()]
        self.assertEqual(kategori, ["REQUEST", "PROCESS"])

    def test_catat_blocked(self):
        self.logger.catat_blocked("BJ-01", 2)
        _, kat, pesan = self.logger.get_entries()[0]
        self.assertEqual(kat, "BLOCKED")
        self.assertIn("2 material", pesan)

    def test_catat_error(self):
        self.logger.catat_error("Overflow: tumpukan penuh")
        self.assertEqual(self.logger.get_entries()[0][1], "ERROR")

    def test_filter_kategori(self):
        self.logger.catat_push("A", "a", 1)
        self.logger.catat_pop("A", "a")
        self.logger.catat_push("B", "b", 2)
        self.assertEqual(len(self.logger.get_entries("PUSH")), 2)
        self.assertEqual(len(self.logger.get_entries("pop")), 1)
        self.assertEqual(self.logger.get_entries("ERROR"), [])

    def test_tampil_riwayat_kosong(self):
        self.assertIn("Belum ada aktivitas", tangkap_riwayat(self.logger))

    def test_tampil_riwayat_format(self):
        self.logger.catat_push("BJ-01", "Baja", 5)
        keluaran = tangkap_riwayat(self.logger)
        baris = [b for b in keluaran.splitlines() if "PUSH" in b][0]
        self.assertRegex(baris, r"^\s*1\. \[" + POLA_WAKTU + r"\] PUSH\s+\| Material BJ-01")
        self.assertIn("Total ditampilkan: 1 dari 1 catatan", keluaran)

    def test_tampil_limit_n_terakhir(self):
        for i in range(10):
            self.logger.log("INFO", f"pesan-{i}")
        keluaran = tangkap_riwayat(self.logger, limit=3)
        self.assertIn("pesan-9", keluaran)
        self.assertIn("pesan-7", keluaran)
        self.assertNotIn("pesan-6", keluaran)
        self.assertIn("3 dari 10", keluaran)

    def test_tampil_filter_kategori(self):
        self.logger.catat_push("A", "a", 1)
        self.logger.catat_blocked("A", 1)
        keluaran = tangkap_riwayat(self.logger, kategori="BLOCKED")
        self.assertIn("BLOCKED", keluaran)
        self.assertNotIn("PUSH ", keluaran)

    def test_skenario_lengkap_bongkar_muat(self):
        self.logger.catat_push("BJ-01", "Baja", 10)
        self.logger.catat_push("BJ-02", "Kontainer", 20)
        self.logger.catat_permintaan("BJ-01")
        self.logger.catat_blocked("BJ-01", 1)
        self.logger.catat_pop("BJ-02", "Kontainer")
        self.logger.catat_proses("BJ-01")
        kategori = [e[1] for e in self.logger.get_entries()]
        self.assertEqual(
            kategori, ["PUSH", "PUSH", "REQUEST", "BLOCKED", "POP", "PROCESS"]
        )


if __name__ == "__main__":
    unittest.main()