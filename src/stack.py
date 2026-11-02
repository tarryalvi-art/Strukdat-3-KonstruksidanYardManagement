from typing import Any, Optional

from node import Node


class StackEmptyError(Exception):
    """Underflow: pop/peek pada stack kosong."""


class StackFullError(Exception):
    """Overflow: push pada stack penuh."""


class Stack:
    def __init__(self, capacity: Optional[int] = None) -> None:
        if capacity is not None and capacity <= 0:
            raise ValueError("Kapasitas harus lebih dari 0.")
        self._top = None
        self._size = 0
        self._capacity = capacity

    def push(self, item: Any) -> None:
        if self.is_full():
            raise StackFullError(f"Stack penuh (kapasitas {self._capacity}).")
        self._top = Node(item, self._top)
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise StackEmptyError("Stack kosong, tidak bisa pop.")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.data

    def peek(self) -> Any:
        if self.is_empty():
            raise StackEmptyError("Stack kosong, tidak bisa peek.")
        return self._top.data

    def is_empty(self) -> bool:
        return self._top is None

    def is_full(self) -> bool:
        return self._capacity is not None and self._size >= self._capacity

    def size(self) -> int:
        return self._size

    def items_above(self, item: Any) -> list:
        """Item di atas `item` (dari paling atas); kosong = tidak terblokir."""
        hasil, cur = [], self._top
        while cur:
            if cur.data == item:
                return hasil
            hasil.append(cur.data)
            cur = cur.next
        raise ValueError(f"{item!r} tidak ada di stack.")

    def __iter__(self):
        cur = self._top
        while cur:
            yield cur.data
            cur = cur.next

    def __len__(self) -> int:
        return self._size
