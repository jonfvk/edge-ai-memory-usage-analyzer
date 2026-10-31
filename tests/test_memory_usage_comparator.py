import unittest
from edge_ai_memory_usage_analyzer.memory_usage_comparator import MemoryUsageComparator

class TestMemoryUsageComparator(unittest.TestCase):
    def test_fits_in_memory_exact(self):
        comp = MemoryUsageComparator(total_usage_bytes=1024, device_total_bytes=1024)
        self.assertTrue(comp.fits_in_memory())
        self.assertEqual(comp.overflow_bytes(), 0)
        summary = comp.summary()
        self.assertTrue(summary['fits'])
        self.assertEqual(summary['overflow_bytes'], 0)
        self.assertIn('fits within device memory', comp.summary_str())

    def test_fits_in_memory_under(self):
        comp = MemoryUsageComparator(total_usage_bytes=512, device_total_bytes=1024)
        self.assertTrue(comp.fits_in_memory())
        self.assertEqual(comp.overflow_bytes(), 0)
        summary = comp.summary()
        self.assertTrue(summary['fits'])
        self.assertEqual(summary['overflow_bytes'], 0)
        self.assertIn('fits within device memory', comp.summary_str())

    def test_overflow(self):
        comp = MemoryUsageComparator(total_usage_bytes=2048, device_total_bytes=1024)
        self.assertFalse(comp.fits_in_memory())
        self.assertEqual(comp.overflow_bytes(), 1024)
        summary = comp.summary()
        self.assertFalse(summary['fits'])
        self.assertEqual(summary['overflow_bytes'], 1024)
        self.assertIn('exceeds device memory', comp.summary_str())
        self.assertIn('by 1.00 KB', comp.summary_str())

    def test_bytes_to_str(self):
        self.assertEqual(MemoryUsageComparator.bytes_to_str(123), '123 B')
        self.assertEqual(MemoryUsageComparator.bytes_to_str(2048), '2.00 KB')
        self.assertEqual(MemoryUsageComparator.bytes_to_str(5 * 1024 ** 2), '5.00 MB')
        self.assertEqual(MemoryUsageComparator.bytes_to_str(3 * 1024 ** 3), '3.00 GB')

    def test_invalid_total_usage_bytes(self):
        with self.assertRaises(ValueError):
            MemoryUsageComparator(-1, 1024)
        with self.assertRaises(ValueError):
            MemoryUsageComparator('bad', 1024)

    def test_invalid_device_total_bytes(self):
        with self.assertRaises(ValueError):
            MemoryUsageComparator(1024, 0)
        with self.assertRaises(ValueError):
            MemoryUsageComparator(1024, -100)
        with self.assertRaises(ValueError):
            MemoryUsageComparator(1024, 'bad')

if __name__ == '__main__':
    unittest.main()
