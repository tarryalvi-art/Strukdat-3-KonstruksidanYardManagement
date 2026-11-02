import math
 
 
class ValidationError(ValueError):
    """Data input material atau permintaan tidak valid."""
 
 
class MaterialValidator:
    @staticmethod
    def _cek_kode(kode):
        if not isinstance(kode, str) or not kode.strip():
            raise ValidationError("Kode material tidak boleh kosong dan harus berupa teks.")
        return kode.strip()
 
    @staticmethod
    def validate_material_data(kode, nama, berat):
        """Validasi material baru (sebelum masuk Stack). Mengembalikan data bersih."""
        kode = MaterialValidator._cek_kode(kode)
        if not isinstance(nama, str) or not nama.strip():
            raise ValidationError("Nama material tidak boleh kosong dan harus berupa teks.")
        if isinstance(berat, bool) or not isinstance(berat, (int, float)):
            raise ValidationError("Berat material harus berupa angka.")
        if not math.isfinite(berat) or berat <= 0:
            raise ValidationError("Berat material harus angka lebih besar dari 0.")
        return {"kode": kode, "nama": nama.strip(), "berat": berat}
 
    @staticmethod
    def validate_request_data(kode):
        """Validasi permintaan material (sebelum masuk Queue). Mengembalikan kode bersih."""
        try:
            return MaterialValidator._cek_kode(kode)
        except ValidationError as e:
            raise ValidationError(f"Permintaan material gagal: {e}")
 
