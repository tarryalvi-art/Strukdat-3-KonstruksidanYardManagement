import os
import sys
import unittest
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
 
from validator import MaterialValidator as V, ValidationError
 
 
class TestMaterialValidator(unittest.TestCase):
    def test_input_benar_dan_dibersihkan(self):
        hasil = V.validate_material_data(" BJ-01 ", " Baja H-Beam ", 12.5)
        self.assertEqual(hasil, {"kode": "BJ-01", "nama": "Baja H-Beam", "berat": 12.5})
 
    def test_kode_salah(self):
        for kode in ["", "   ", None, 123]:
            with self.assertRaises(ValidationError):
                V.validate_material_data(kode, "Baja", 10)
 
    def test_nama_salah(self):
        for nama in ["", "   ", None, 5]:
            with self.assertRaises(ValidationError):
                V.validate_material_data("BJ-01", nama, 10)
 
    def test_berat_salah(self):
        for berat in [0, -5, "sepuluh", None, True, float("nan"), float("inf")]:
            with self.assertRaises(ValidationError):
                V.validate_material_data("BJ-01", "Baja", berat)
 
    def test_permintaan(self):
        self.assertEqual(V.validate_request_data(" BJ-01 "), "BJ-01")
        with self.assertRaises(ValidationError) as e:
            V.validate_request_data("")
        self.assertIn("Permintaan material gagal", str(e.exception))
 
    def test_validation_error_adalah_value_error(self):
        self.assertTrue(issubclass(ValidationError, ValueError))
 
 
if __name__ == "__main__":
    unittest.main()
 
