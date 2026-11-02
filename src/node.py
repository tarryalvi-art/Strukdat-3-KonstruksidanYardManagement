from __future__ import annotations

from typing import Any, Optional


class Node:
    def __init__(self, data: Any, next: Optional["Node"] = None) -> None:
        self._data = data
        self._next = next

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, value: Any) -> None:
        self._data = value

    @property
    def next(self) -> Optional["Node"]:
        return self._next

    @next.setter
    def next(self, node: Optional["Node"]) -> None:
        self._next = node

    def __repr__(self) -> str:
        return f"Node(data={self._data!r})"