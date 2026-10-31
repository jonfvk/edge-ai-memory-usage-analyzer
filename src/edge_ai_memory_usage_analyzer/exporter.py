import os
from datetime import datetime

class Exporter:
    """
    Exports memory usage analysis results to a text file.
    Accepts all relevant scenario data and writes a readable report.
    """
    DEFAULT_FILENAME = "memory_usage_report.txt"

    @staticmethod
    def export(
        filepath,
        device_specs,
        scenarios,
        created_by="Edge AI Memory Usage Analyzer",
        notes=None
    ):
        """
        Write a report to the given filepath.

        Args:
            filepath (str): Path to the output text file.
            device_specs (DeviceSpecs): DeviceSpecs instance.
            scenarios (list of dict): Each dict should have:
                - 'model_size_bytes' (int)
                - 'input_data_size_bytes' (int)
                - 'total_usage_bytes' (int)
                - 'fits' (bool)
                - 'overflow_bytes' (int)
                - 'summary_str' (str)
                - 'suggestions' (list of str, optional)
            created_by (str): Tool or user info.
            notes (str|None): Optional notes to include.
        """
        def bytes_to_str(b):
            if b >= 1024 ** 3:
                return f"{b / 1024 ** 3:.2f} GB"
            elif b >= 1024 ** 2:
                return f"{b / 1024 ** 2:.2f} MB"
            elif b >= 1024:
                return f"{b / 1024:.2f} KB"
            else:
                return f"{b} B"

        lines = []
        lines.append(f"Memory Usage Analysis Report")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Created by: {created_by}")
        lines.append("")
        lines.append(f"Device: {device_specs.get_total_memory_str()} {device_specs.get_memory_type()}")
        lines.append("")
        if notes:
            lines.append("Notes:")
            lines.append(notes)
            lines.append("")
        for idx, sc in enumerate(scenarios):
            lines.append(f"Scenario {idx+1}:")
            lines.append(f"  Model size:      {bytes_to_str(sc['model_size_bytes'])}")
            lines.append(f"  Input data size: {bytes_to_str(sc['input_data_size_bytes'])}")
            lines.append(f"  Total usage:     {bytes_to_str(sc['total_usage_bytes'])}")
            lines.append(f"  Fits in memory:  {'YES' if sc['fits'] else 'NO'}")
            if not sc['fits']:
                lines.append(f"  Overflow:        {bytes_to_str(sc['overflow_bytes'])}")
            lines.append(f"  Summary:         {sc['summary_str']}")
            if 'suggestions' in sc and sc['suggestions']:
                lines.append("  Suggestions:")
                for sugg in sc['suggestions']:
                    lines.append(f"    - {sugg}")
            lines.append("")
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return filepath
