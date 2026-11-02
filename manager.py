from stack import Stack, StackEmptyError


class StackManager:
    """Pengelola sederhana yang memakai Stack (linked list dari Node)."""

    def __init__(self):
        self.stack = Stack()

    def tambah(self, item):
        self.stack.push(item)
        return f"'{item}' ditambahkan."

    def hapus(self):
        try:
            item = self.stack.pop()
            return f"'{item}' dihapus."
        except StackEmptyError:
            return "Stack kosong, tidak ada yang dihapus."

    def lihat_atas(self):
        try:
            return self.stack.peek()
        except StackEmptyError:
            return None

    def cari(self, item):
        # `in` bekerja karena Stack punya __iter__
        return item in self.stack

    def balik(self):
        # to_list() urutannya dari atas ke bawah; push ulang membalik urutan
        items = self.stack.to_list()
        self.stack.clear()
        for item in items:
            self.stack.push(item)

    def kosongkan(self):
        self.stack.clear()

    def jumlah(self):
        return len(self.stack)

    def tampilkan(self):
        if self.stack.is_empty():
            return "Stack kosong."
        return "Atas -> " + " | ".join(str(x) for x in self.stack) + " <- Bawah"


if __name__ == "__main__":
    m = StackManager()
    print(m.tambah("A"))
    print(m.tambah("B"))
    print(m.tambah("C"))
    print(m.tampilkan())
    print(m.hapus())
    print(m.tampilkan())