class ValidationError(Exception):
    """Exception khusus jika data input material salah."""
    pass


class MaterialValidator:
    @staticmethod
    def validate_material_data(name: str, quantity: int) -> dict:
        """
        Referensi Validasi untuk Input Material Baru (Masuk Gudang).
        Digunakan oleh Anggota 3 sebelum dimasukkan ke Stack.
        """
        # 1. Cek apakah nama kosong atau bukan teks
        if not name or not isinstance(name, str):
            raise ValidationError("Nama material tidak boleh kosong dan harus berupa teks.")
        
        clean_name = name.strip()
        if len(clean_name) == 0:
            raise ValidationError("Nama material tidak boleh hanya berisi spasi.")

        # 2. Cek apakah jumlah material valid (harus angka positif)
        if quantity is None:
            raise ValidationError("Jumlah material harus diisi.")
            
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValidationError("Jumlah material harus berupa angka bulat yang valid.")
            
        if quantity <= 0:
            raise ValidationError("Jumlah material harus lebih besar dari 0.")

        # Jika lolos semua, kembalikan data bersih berformat Dictionary
        return {
            "name": clean_name,
            "quantity": quantity
        }

    @staticmethod
    def validate_request_data(name: str, quantity: int) -> dict:
        """
        Referensi Validasi untuk Permintaan Material (Keluar Gudang).
        Digunakan oleh Anggota 3 sebelum dimasukkan ke Queue.
        """
        try:
            return MaterialValidator.validate_material_data(name, quantity)
        except ValidationError as e:
            raise ValidationError(f"Permintaan material gagal: {str(e)}")

    @staticmethod
    def safe_validate(name: str, quantity: int) -> tuple[bool, str | dict]:
        """
        Fungsi Penanganan Error Aman (Supaya program utama Anggota 6 tidak mendadak berhenti/crash).
        Mengembalikan: (Status_Sukses, Data_Bersih_Atau_Pesan_Error)
        """
        try:
            data = MaterialValidator.validate_material_data(name, quantity)
            return True, data
        except ValidationError as e:
            return False, str(e)