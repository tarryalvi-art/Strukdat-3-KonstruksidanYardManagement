import os
import sys
import unittest
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
 
from yard_queue import Queue, QueueEmptyError, QueueFullError
 
 
class TestQueue(unittest.TestCase):
    def test_fifo(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        for x in "ABC":
            q.enqueue(x)
        self.assertEqual(q.peek(), "A")
        self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], ["A", "B", "C"])
        self.assertTrue(q.is_empty())
 
    def test_enqueue_setelah_kosong(self):
        q = Queue()
        q.enqueue("A")
        q.dequeue()
        q.enqueue("B")
        self.assertEqual(q.peek(), "B")
        self.assertEqual(list(q), ["B"])
 
    def test_antrean_kosong(self):
        with self.assertRaises(QueueEmptyError):
            Queue().dequeue()
        with self.assertRaises(QueueEmptyError):
            Queue().peek()
 
    def test_overflow(self):
        q = Queue(capacity=1)
        q.enqueue("A")
        with self.assertRaises(QueueFullError):
            q.enqueue("B")
        q.dequeue()
        q.enqueue("B")
        self.assertEqual(len(q), 1)
 
    def test_kapasitas_tidak_valid(self):
        with self.assertRaises(ValueError):
            Queue(capacity=0)
 
 
if __name__ == "__main__":
    unittest.main()
