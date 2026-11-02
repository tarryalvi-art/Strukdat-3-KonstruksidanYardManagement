import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from node import Node
from stack import Stack, StackEmptyError


def test_node():
    print("--- Test Node ---")
    n1 = Node("Baja-001")
    n2 = Node("Kontainer-002", next=n1)

    assert n1.data == "Baja-001"
    assert n1.next is None
    assert n2.next is n1

    n1.data = "Baja-Edit"
    assert n1.data == "Baja-Edit"
    print("Node OK:", n1, n2)


def test_stack_dasar():
    print("--- Test operasi dasar Stack ---")
    s = Stack()
    assert s.is_empty() is True
    assert s.size() == 0

    s.push("Baja A")
    s.push("Baja B")
    s.push("Kontainer C")

    assert s.is_empty() is False
    assert s.size() == 3
    assert s.peek() == "Kontainer C"

    assert s.pop() == "Kontainer C"
    assert s.pop() == "Baja B"
    assert s.peek() == "Baja A"
    assert s.size() == 1

    assert s.pop() == "Baja A"
    assert s.is_empty() is True
    print("Urutan LIFO benar. Stack dasar OK.")


def test_underflow():
    print("--- Test underflow ---")
    s = Stack()

    try:
        s.pop()
        print("GAGAL: seharusnya error")
    except StackEmptyError as e:
        print("pop kosong error:", e)

    try:
        s.peek()
        print("GAGAL: seharusnya error")
    except StackEmptyError as e:
        print("peek kosong error:", e)

    for i in range(1000):
        s.push(i)
    for i in range(999, -1, -1):
        assert s.pop() == i
    assert s.is_empty()
    print("Stress test 1000 push/pop OK.")


def test_utilitas():
    print("--- Test utilitas ---")
    s = Stack()
    for item in ["A", "B", "C"]:
        s.push(item)

    assert list(s) == ["C", "B", "A"]
    assert s.to_list() == ["C", "B", "A"]
    assert len(s) == 3

    s.clear()
    assert s.is_empty() and s.size() == 0
    print("Utilitas OK:", s)


if __name__ == "__main__":
    test_node()
    test_stack_dasar()
    test_underflow()
    test_utilitas()
    print("\nSemua test Stack lulus.")
