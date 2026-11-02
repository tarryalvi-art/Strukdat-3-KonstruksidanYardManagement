import os
import sys
import unittest
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
 
from stack import Stack, StackEmptyError, StackFullError
 
 
class TestStack(unittest.TestCase):
    def test_lifo(self):
        s = Stack()
        for x in "ABC":
            s.push(x)
        self.assertEqual(s.peek(), "C")
        self.assertEqual([s.pop(), s.pop(), s.pop()], ["C", "B", "A"])
        self.assertTrue(s.is_empty())
 
    def test_underflow(self):
        with self.assertRaises(StackEmptyError):
            Stack().pop()
        with self.assertRaises(StackEmptyError):
            Stack().peek()
 
    def test_overflow(self):
        s = Stack(capacity=1)
        s.push("A")
        with self.assertRaises(StackFullError):
            s.push("B")
        s.pop()
        s.push("B")
        self.assertEqual(s.peek(), "B")
 
    def test_kapasitas_tidak_valid(self):
        with self.assertRaises(ValueError):
            Stack(capacity=0)
 
    def test_items_above(self):
        s = Stack()
        for x in ["Baja", "Kontainer", "Pipa"]:
            s.push(x)
        self.assertEqual(s.items_above("Pipa"), [])
        self.assertEqual(s.items_above("Baja"), ["Pipa", "Kontainer"])
        self.assertEqual(len(s), 3)
        with self.assertRaises(ValueError):
            s.items_above("Beton")
 
 
if __name__ == "__main__":
    unittest.main()
 
