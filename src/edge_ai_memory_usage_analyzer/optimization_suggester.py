class OptimizationSuggester:
    """
    Suggests possible optimizations if memory usage exceeds device memory.
    Suggestions are based on model size, input data size, and overflow amount.
    """
    def __init__(self, model_size_bytes, input_data_size_bytes, device_total_bytes):
        if not all(isinstance(x, int) and x >= 0 for x in [model_size_bytes, input_data_size_bytes]):
            raise ValueError("Model and input data sizes must be non-negative integers")
        if not isinstance(device_total_bytes, int) or device_total_bytes <= 0:
            raise ValueError("Device total bytes must be a positive integer")
        self.model_size_bytes = model_size_bytes
        self.input_data_size_bytes = input_data_size_bytes
        self.device_total_bytes = device_total_bytes
        self.total_usage_bytes = model_size_bytes + input_data_size_bytes
        self.overflow_bytes = max(0, self.total_usage_bytes - device_total_bytes)

    def suggest(self):
        """
        Returns a list of suggestion strings for reducing memory usage.
        If usage fits, returns an empty list.
        """
        if self.overflow_bytes == 0:
            return []
        suggestions = []
        # Suggest model optimizations
        if self.model_size_bytes > 0:
            suggestions.append(
                "Reduce model size: try quantization, pruning, or using a smaller architecture."
            )
        # Suggest input data optimizations
        if self.input_data_size_bytes > 0:
            suggestions.append(
                "Reduce input data size: use lower resolution, batch size, or compress input data."
            )
        # Suggest device upgrade if overflow is very large
        if self.overflow_bytes > self.device_total_bytes * 0.5:
            suggestions.append(
                "Consider using a device with more memory if possible."
            )
        # Suggest mixed precision if model is large
        if self.model_size_bytes > 10 * 1024 * 1024:  # >10MB
            suggestions.append(
                "Use mixed precision (e.g., float16) to reduce model memory footprint."
            )
        # Suggest streaming input if data is large
        if self.input_data_size_bytes > 10 * 1024 * 1024:
            suggestions.append(
                "Stream input data instead of loading all at once, if applicable."
            )
        # Suggest memory mapping for very large models
        if self.model_size_bytes > 50 * 1024 * 1024:
            suggestions.append(
                "Use memory-mapped model loading if supported by your framework."
            )
        return suggestions

    def suggest_str(self):
        """
        Returns suggestions as a formatted string, or an empty string if none.
        """
        suggestions = self.suggest()
        if not suggestions:
            return ""
        return "Possible optimizations to reduce memory usage:\n- " + "\n- ".join(suggestions)
