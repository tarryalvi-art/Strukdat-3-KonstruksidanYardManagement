from typing import Any, Optional
 
from node import Node
 
 
class QueueEmptyError(Exception):
    """Underflow: dequeue/peek pada antrean kosong."""
 
 
class QueueFullError(Exception):
    """Overflow: enqueue pada antrean penuh."""
 
 
class Queue:
    """Antrean FIFO berbasis linked list (Node kustom)."""
 
    def __init__(self, capacity: Optional[int] = None) -> None:
        if capacity is not None and capacity <= 0:
            raise ValueError("Kapasitas harus lebih dari 0.")
        self._front = None
        self._rear = None
        self._size = 0
        self._capacity = capacity
 
    def enqueue(self, item: Any) -> None:
        if self.is_full():
            raise QueueFullError(f"Antrean penuh (kapasitas {self._capacity}).")
        node = Node(item)
        if self._rear:
            self._rear.next = node
        else:
            self._front = node
        self._rear = node
        self._size += 1
 
    def dequeue(self) -> Any:
        if self.is_empty():
            raise QueueEmptyError("Antrean kosong, tidak bisa dequeue.")
        node = self._front
        self._front = node.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return node.data
 
    def peek(self) -> Any:
        if self.is_empty():
            raise QueueEmptyError("Antrean kosong, tidak bisa peek.")
        return self._front.data
 
    def is_empty(self) -> bool:
        return self._front is None
 
    def is_full(self) -> bool:
        return self._capacity is not None and self._size >= self._capacity
 
    def size(self) -> int:
        return self._size
 
    def __iter__(self):
        cur = self._front
        while cur:
            yield cur.data
            cur = cur.next
 
    def __len__(self) -> int:
        return self._size
