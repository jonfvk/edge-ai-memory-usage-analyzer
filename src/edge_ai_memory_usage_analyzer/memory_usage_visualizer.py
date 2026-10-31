import math

class MemoryUsageVisualizer:
    """
    Visualizes the memory usage breakdown for model and input data.
    Provides a simple ASCII bar chart and percentage breakdown.
    """
    BAR_WIDTH = 40
    BAR_CHAR_MODEL = '#'
    BAR_CHAR_DATA = '='
    BAR_CHAR_FREE = '-'

    def __init__(self, model_size_bytes, input_data_size_bytes, device_total_bytes):
        if not all(isinstance(x, int) and x >= 0 for x in [model_size_bytes, input_data_size_bytes]):
            raise ValueError("Model and input data sizes must be non-negative integers")
        if not isinstance(device_total_bytes, int) or device_total_bytes <= 0:
            raise ValueError("Device total bytes must be a positive integer")
        self.model_size_bytes = model_size_bytes
        self.input_data_size_bytes = input_data_size_bytes
        self.device_total_bytes = device_total_bytes
        self.total_usage_bytes = model_size_bytes + input_data_size_bytes
        self.free_bytes = max(0, device_total_bytes - self.total_usage_bytes)

    @staticmethod
    def bytes_to_str(num_bytes):
        b = num_bytes
        if b >= 1024 ** 3:
            return f"{b / 1024 ** 3:.2f} GB"
        elif b >= 1024 ** 2:
            return f"{b / 1024 ** 2:.2f} MB"
        elif b >= 1024:
            return f"{b / 1024:.2f} KB"
        else:
            return f"{b} B"

    def breakdown_percentages(self):
        total = self.device_total_bytes
        model_pct = (self.model_size_bytes / total) * 100 if total > 0 else 0
        data_pct = (self.input_data_size_bytes / total) * 100 if total > 0 else 0
        used = self.model_size_bytes + self.input_data_size_bytes
        free_pct = max(0, (self.device_total_bytes - used) / total * 100) if total > 0 else 0
        return {
            'model_pct': model_pct,
            'input_data_pct': data_pct,
            'free_pct': free_pct
        }

    def ascii_bar(self):
        total = self.device_total_bytes
        used = min(self.total_usage_bytes, total)
        model_len = int(round(self.BAR_WIDTH * min(self.model_size_bytes, total) / total)) if total > 0 else 0
        data_len = int(round(self.BAR_WIDTH * min(self.input_data_size_bytes, total - self.model_size_bytes) / total)) if total > 0 else 0
        # Adjust for overflow
        if model_len + data_len > self.BAR_WIDTH:
            data_len = max(0, self.BAR_WIDTH - model_len)
        free_len = self.BAR_WIDTH - model_len - data_len
        bar = (
            self.BAR_CHAR_MODEL * model_len +
            self.BAR_CHAR_DATA * data_len +
            self.BAR_CHAR_FREE * free_len
        )
        return bar

    def breakdown_str(self):
        pct = self.breakdown_percentages()
        lines = []
        lines.append("Memory Usage Breakdown:")
        lines.append(f"  Model:      {self.bytes_to_str(self.model_size_bytes):>10}  ({pct['model_pct']:.1f}%)")
        lines.append(f"  Input Data: {self.bytes_to_str(self.input_data_size_bytes):>10}  ({pct['input_data_pct']:.1f}%)")
        lines.append(f"  Free:       {self.bytes_to_str(self.free_bytes):>10}  ({pct['free_pct']:.1f}%)")
        lines.append("")
        lines.append(f"[{self.ascii_bar()}]")
        legend = (
            f"Legend: {self.BAR_CHAR_MODEL} = Model, "
            f"{self.BAR_CHAR_DATA} = Input Data, "
            f"{self.BAR_CHAR_FREE} = Free"
        )
        lines.append(legend)
        if self.total_usage_bytes > self.device_total_bytes:
            over = self.total_usage_bytes - self.device_total_bytes
            lines.append("")
            lines.append(f"WARNING: Usage exceeds device memory by {self.bytes_to_str(over)}!")
        return "\n".join(lines)

    def as_dict(self):
        pct = self.breakdown_percentages()
        return {
            'model_size_bytes': self.model_size_bytes,
            'input_data_size_bytes': self.input_data_size_bytes,
            'free_bytes': self.free_bytes,
            'device_total_bytes': self.device_total_bytes,
            'model_pct': pct['model_pct'],
            'input_data_pct': pct['input_data_pct'],
            'free_pct': pct['free_pct'],
            'ascii_bar': self.ascii_bar(),
            'warning': self.total_usage_bytes > self.device_total_bytes
        }
