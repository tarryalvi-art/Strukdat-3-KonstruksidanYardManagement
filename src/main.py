from logger import Logger
from manager import YardManager, MaterialBlokirError
from stack import StackEmptyError, StackFullError
from validator import MaterialValidator
from yard_queue import QueueEmptyError
 
KAPASITAS = 10  # area tumpukan terbatas
ERROR = (ValueError, StackEmptyError, StackFullError, QueueEmptyError, MaterialBlokirError)
 
MENU = """
=== YARD MANAGEMENT ===
1. Tambah material ke tumpukan
2. Ambil material teratas
3. Ajukan permintaan material
4. Proses permintaan terdepan
5. Lihat tumpukan
6. Lihat antrean permintaan
7. Riwayat aktivitas
0. Keluar"""
 
 
def tambah(m):
    kode = input("Kode material : ")
    nama = input("Nama material : ")
    try:
        berat = float(input("Berat (ton)   : "))
    except ValueError:
        raise ValueError("Berat harus berupa angka.")
    print(f"Berhasil menumpuk {m.tambah_material(kode, nama, berat)}.")
 
 
AKSI = {
    "1": tambah,
    "2": lambda m: print(f"Diambil: {m.ambil_material()}"),
    "3": lambda m: print(f"Permintaan diajukan: {m.ajukan_permintaan(input('Kode material : '))}"),
    "4": lambda m: print(f"Permintaan diproses, material {m.proses_permintaan()} keluar."),
    "5": lambda m: print("Tumpukan (atas -> bawah):", m.lihat_tumpukan() or "kosong"),
    "6": lambda m: print("Antrean (depan -> belakang):", m.lihat_antrean() or "kosong"),
    "7": lambda m: m.logger.show_history(),
}
 
 
def main():
    manager = YardManager(KAPASITAS, Logger(), MaterialValidator)
    try:
        while True:
            print(MENU)
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0":
                print("Terima kasih.")
                break
            if pilihan not in AKSI:
                print("[!] Menu tidak valid.")
                continue
            try:
                AKSI[pilihan](manager)
            except ERROR as e:
                print(f"[!] {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
 
 
if __name__ == "__main__":
    main()
 