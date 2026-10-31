import unittest
from edge_ai_memory_usage_analyzer.device_specs import DeviceSpecs
from edge_ai_memory_usage_analyzer.input_handler import InputHandler
from edge_ai_memory_usage_analyzer.memory_usage_calculator import MemoryUsageCalculator
from edge_ai_memory_usage_analyzer.memory_usage_comparator import MemoryUsageComparator

class TestMultiScenario(unittest.TestCase):
    def setUp(self):
        # Device: 1GB LPDDR5X
        self.device = DeviceSpecs('1GB', 'LPDDR5X')
        self.device_bytes = self.device.get_total_memory_bytes()
        self.ih = InputHandler()

    def test_multiple_scenarios(self):
        # Define multiple model/data scenarios
        scenarios = [
            {'model': '100MB', 'data': '200MB'},
            {'model': '300MB', 'data': '600MB'},
            {'model': '900MB', 'data': '200MB'},  # Exceeds
            {'model': '512MB', 'data': '512MB'},  # Exactly fits
            {'model': '0', 'data': '0'},          # Minimal
        ]
        results = []
        for idx, sc in enumerate(scenarios):
            model_b, data_b = self.ih.get_model_and_data_size(sc['model'], sc['data'])
            calc = MemoryUsageCalculator(model_b, data_b)
            total_b = calc.total_memory_usage_bytes()
            comp = MemoryUsageComparator(total_b, self.device_bytes)
            results.append({
                'scenario': idx,
                'model_bytes': model_b,
                'data_bytes': data_b,
                'total_bytes': total_b,
                'fits': comp.fits_in_memory(),
                'overflow_bytes': comp.overflow_bytes(),
            })
        # Check results
        self.assertTrue(results[0]['fits'])
        self.assertTrue(results[1]['fits'])
        self.assertFalse(results[2]['fits'])
        self.assertTrue(results[3]['fits'])
        self.assertTrue(results[4]['fits'])
        # Check overflow for scenario 2 (index 2)
        self.assertGreater(results[2]['overflow_bytes'], 0)
        # Scenario 3 should fit exactly
        self.assertEqual(results[3]['overflow_bytes'], 0)
        # Scenario 4 should be minimal
        self.assertEqual(results[4]['total_bytes'], 0)

    def test_empty_scenarios(self):
        # Should handle empty scenario list
        scenarios = []
        results = []
        for sc in scenarios:
            model_b, data_b = self.ih.get_model_and_data_size(sc['model'], sc['data'])
            calc = MemoryUsageCalculator(model_b, data_b)
            total_b = calc.total_memory_usage_bytes()
            comp = MemoryUsageComparator(total_b, self.device_bytes)
            results.append(comp.fits_in_memory())
        self.assertEqual(results, [])

    def test_invalid_scenario(self):
        # Should raise ValueError for invalid input
        scenarios = [
            {'model': '-10MB', 'data': '100MB'},
            {'model': '100MB', 'data': '-1'},
            {'model': 'bad', 'data': '100MB'},
        ]
        for sc in scenarios:
            with self.assertRaises(ValueError):
                self.ih.get_model_and_data_size(sc['model'], sc['data'])

if __name__ == '__main__':
    unittest.main()
