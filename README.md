# Edge AI Memory Usage Analyzer

Analyze and visualize memory usage for AI models on edge devices, ensuring models fit within device constraints.

## Overview

Edge AI devices have strict memory limits. This tool helps developers estimate and visualize the total memory usage of their AI models and input data, compare it to device memory limits, and receive warnings and optimization suggestions if usage exceeds available memory.

## Features
- Accepts model and input data sizes in bytes, KB, MB, or GB
- Supports multiple device memory specifications (e.g., 8GB LPDDR5X)
- Calculates total memory usage
- Compares usage to device memory limit
- Warns if usage exceeds available memory
- Suggests possible optimizations
- Visualizes memory usage breakdown (ASCII bar chart)
- Allows multiple model/data scenarios
- Exports results to a text file

## Installation

This tool is a pure Python package. No external dependencies are required.

1. Clone or download this repository.
2. Ensure Python 3.7+ is installed.
3. Add `src/` to your `PYTHONPATH` or install as a package if desired.

## Usage Example

Below is a minimal example of how to use the tool programmatically:

```python
from edge_ai_memory_usage_analyzer.device_specs import DeviceSpecs
from edge_ai_memory_usage_analyzer.input_handler import InputHandler
from edge_ai_memory_usage_analyzer.memory_usage_calculator import MemoryUsageCalculator
from edge_ai_memory_usage_analyzer.memory_usage_comparator import MemoryUsageComparator
from edge_ai_memory_usage_analyzer.memory_usage_visualizer import MemoryUsageVisualizer
from edge_ai_memory_usage_analyzer.optimization_suggester import OptimizationSuggester
from edge_ai_memory_usage_analyzer.exporter import Exporter

# 1. Define device memory specs
specs = DeviceSpecs('8GB', 'LPDDR5X')

# 2. Input model and data sizes
ih = InputHandler()
model_size_bytes, input_data_size_bytes = ih.get_model_and_data_size('120MB', '300MB')

# 3. Calculate total memory usage
calc = MemoryUsageCalculator(model_size_bytes, input_data_size_bytes)
total_usage_bytes = calc.total_memory_usage_bytes()

# 4. Compare to device memory
comp = MemoryUsageComparator(total_usage_bytes, specs.get_total_memory_bytes())
print(comp.summary_str())

# 5. Warn if usage exceeds memory
if not comp.fits_in_memory():
    print('WARNING: Memory usage exceeds device limit!')

# 6. Suggest optimizations
sugg = OptimizationSuggester(model_size_bytes, input_data_size_bytes, specs.get_total_memory_bytes())
for suggestion in sugg.suggest():
    print('Suggestion:', suggestion)

# 7. Visualize memory usage
viz = MemoryUsageVisualizer(model_size_bytes, input_data_size_bytes, specs.get_total_memory_bytes())
print(viz.breakdown_str())
print(viz.ascii_bar())

# 8. Export results to text file
scenario = {
    'model_size_bytes': model_size_bytes,
    'input_data_size_bytes': input_data_size_bytes,
    'total_usage_bytes': total_usage_bytes,
    'fits': comp.fits_in_memory(),
    'overflow_bytes': comp.overflow_bytes(),
    'summary_str': comp.summary_str(),
    'suggestions': sugg.suggest(),
}
Exporter.export('memory_usage_report.txt', specs, [scenario])
print('Report exported to memory_usage_report.txt')
```

## Multi-Scenario Analysis

You can analyze multiple model/data scenarios by repeating the above steps for each scenario and passing a list of scenario dictionaries to `Exporter.export()`.

## Testing

Run all tests with:

```
python -m unittest discover tests
```

## File Structure

- `src/edge_ai_memory_usage_analyzer/` - Source code modules
- `tests/` - Unit tests
- `README.md` - This documentation

## Source URLs
- https://techgig.com/news/ai/nvidia-unveils-jetson-orin-nano-2-for-edge-ai-robotics/134930001 (retrieved 2024-06)

## License

This project is provided for educational and developer productivity purposes only.
