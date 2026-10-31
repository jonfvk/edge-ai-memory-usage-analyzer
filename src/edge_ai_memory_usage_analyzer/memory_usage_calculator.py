class MemoryUsageCalculator:
    """
    Calculates total memory usage for a given model and input data size.
    """
    def __init__(self, model_size_bytes, input_data_size_bytes):
        """
        Args:
            model_size_bytes (int): Size of the model in bytes.
            input_data_size_bytes (int): Size of the input data in bytes.
        """
        if not isinstance(model_size_bytes, int) or model_size_bytes < 0:
            raise ValueError("model_size_bytes must be a non-negative integer")
        if not isinstance(input_data_size_bytes, int) or input_data_size_bytes < 0:
            raise ValueError("input_data_size_bytes must be a non-negative integer")
        self.model_size_bytes = model_size_bytes
        self.input_data_size_bytes = input_data_size_bytes

    def total_memory_usage_bytes(self):
        """
        Returns the total memory usage in bytes (int).
        """
        return self.model_size_bytes + self.input_data_size_bytes

    def total_memory_usage_str(self):
        """
        Returns the total memory usage as a human-readable string (e.g., '12.34 MB').
        """
        b = self.total_memory_usage_bytes()
        if b >= 1024 ** 3:
            return f"{b / 1024 ** 3:.2f} GB"
        elif b >= 1024 ** 2:
            return f"{b / 1024 ** 2:.2f} MB"
        elif b >= 1024:
            return f"{b / 1024:.2f} KB"
        else:
            return f"{b} B"

    def as_dict(self):
        """
        Returns a dictionary with breakdown and total usage in bytes and string.
        """
        return {
            'model_size_bytes': self.model_size_bytes,
            'input_data_size_bytes': self.input_data_size_bytes,
            'total_memory_usage_bytes': self.total_memory_usage_bytes(),
            'total_memory_usage_str': self.total_memory_usage_str(),
        }
