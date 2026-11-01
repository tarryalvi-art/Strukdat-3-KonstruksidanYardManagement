from __future__ import annotations

from typing import Any, Iterator, Optional

from node import Node


class StackEmptyError(Exception):
    """Error saat pop/peek dilakukan pada stack kosong."""


class Stack:
    def __init__(self) -> None:
        self._top: Optional[Node] = None
        self._size: int = 0

    def push(self, item: Any) -> None:
        new_node = Node(item)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise StackEmptyError("Stack kosong, tidak bisa pop.")
        popped = self._top
        self._top = popped.next
        popped.next = None
        self._size -= 1
        return popped.data

    def peek(self) -> Any:
        if self.is_empty():
            raise StackEmptyError("Stack kosong, tidak ada item untuk peek.")
        return self._top.data

    def is_empty(self) -> bool:
        return self._top is None

    def size(self) -> int:
        return self._size

    def clear(self) -> None:
        self._top = None
        self._size = 0

    def to_list(self) -> list:
        hasil = []
        current = self._top
        while current is not None:
            hasil.append(current.data)
            current = current.next
        return hasil

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self._top
        while current is not None:
            yield current.data
            current = current.next

    def __repr__(self) -> str:
        return f"Stack(size={self._size}, items={self.to_list()!r})"
    