from manager import StackManager


def test_tambah_dan_jumlah():
    m = StackManager()
    m.tambah(1)
    m.tambah(2)
    assert m.jumlah() == 2
    assert m.lihat_atas() == 2


def test_hapus():
    m = StackManager()
    m.tambah("A")
    m.tambah("B")
    m.hapus()
    assert m.lihat_atas() == "A"
    assert m.jumlah() == 1


def test_hapus_stack_kosong():
    m = StackManager()
    assert m.hapus() == "Stack kosong, tidak ada yang dihapus."
    assert m.lihat_atas() is None


def test_cari():
    m = StackManager()
    m.tambah(10)
    m.tambah(20)
    assert m.cari(10) is True
    assert m.cari(99) is False


def test_balik():
    m = StackManager()
    for x in [1, 2, 3]:
        m.tambah(x)
    # sebelum: atas 3,2,1 -> sesudah: atas 1,2,3
    m.balik()
    assert m.stack.to_list() == [1, 2, 3]


def test_kosongkan():
    m = StackManager()
    m.tambah(1)
    m.kosongkan()
    assert m.jumlah() == 0
    assert m.tampilkan() == "Stack kosong."


def test_tampilkan():
    m = StackManager()
    m.tambah("A")
    m.tambah("B")
    assert m.tampilkan() == "Atas -> B | A <- Bawah"


if __name__ == "__main__":
    daftar_test = [
        test_tambah_dan_jumlah,
        test_hapus,
        test_hapus_stack_kosong,
        test_cari,
        test_balik,
        test_kosongkan,
        test_tampilkan,
    ]
    lolos = 0
    for fungsi in daftar_test:
        try:
            fungsi()
            print(f"[LOLOS] {fungsi.__name__}")
            lolos += 1
        except AssertionError:
            print(f"[GAGAL] {fungsi.__name__}")
    print(f"\n{lolos}/{len(daftar_test)} test lolos")
