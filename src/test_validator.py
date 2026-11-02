import unittest
# Mengimport class dari file validator.py di atas
from validator import MaterialValidator, ValidationError

class TestMaterialValidator(unittest.TestCase):
    
    def test_input_benar(self):
        """Uji coba jika pengguna memasukkan data yang benar."""
        hasil = MaterialValidator.validate_material_data("Semen Tiga Roda", 100)
        self.assertEqual(hasil["name"], "Semen Tiga Roda")
        self.assertEqual(hasil["quantity"], 100)

    def test_nama_kosong(self):
        """Uji coba jika nama material kosong (Harus memunculkan Error)."""
        with self.assertRaises(ValidationError):
            MaterialValidator.validate_material_data("", 10)

    def test_jumlah_minus_atau_nol(self):
        """Uji coba jika kuantitas kurang dari atau sama dengan 0 (Harus memunculkan Error)."""
        with self.assertRaises(ValidationError):
            MaterialValidator.validate_material_data("Besi", 0)
        with self.assertRaises(ValidationError):
            MaterialValidator.validate_material_data("Besi", -5)

    def test_tipe_data_salah(self):
        """Uji coba jika jumlah diisi teks bukan angka bulat."""
        with self.assertRaises(ValidationError):
            MaterialValidator.validate_material_data("Baja", "sepuluh")


if __name__ == "__main__":
    unittest.main()