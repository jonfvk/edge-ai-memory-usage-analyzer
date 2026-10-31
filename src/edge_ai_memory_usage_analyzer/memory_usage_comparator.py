class MemoryUsageComparator:
    """
    Compares total memory usage to device memory limit.
    Provides result and details for fit/overflow.
    """
    def __init__(self, total_usage_bytes, device_total_bytes):
        """
        Args:
            total_usage_bytes (int): Total memory usage in bytes.
            device_total_bytes (int): Device memory limit in bytes.
        """
        if not isinstance(total_usage_bytes, int) or total_usage_bytes < 0:
            raise ValueError("total_usage_bytes must be a non-negative integer")
        if not isinstance(device_total_bytes, int) or device_total_bytes <= 0:
            raise ValueError("device_total_bytes must be a positive integer")
        self.total_usage_bytes = total_usage_bytes
        self.device_total_bytes = device_total_bytes

    def fits_in_memory(self):
        """
        Returns True if total usage fits within device memory, else False.
        """
        return self.total_usage_bytes <= self.device_total_bytes

    def overflow_bytes(self):
        """
        Returns the number of bytes by which usage exceeds device memory.
        Returns 0 if it fits.
        """
        if self.fits_in_memory():
            return 0
        return self.total_usage_bytes - self.device_total_bytes

    def summary(self):
        """
        Returns a dictionary summarizing the comparison.
        """
        return {
            'fits': self.fits_in_memory(),
            'total_usage_bytes': self.total_usage_bytes,
            'device_total_bytes': self.device_total_bytes,
            'overflow_bytes': self.overflow_bytes(),
        }

    @staticmethod
    def bytes_to_str(num_bytes):
        """
        Converts a byte value to a human-readable string.
        """
        b = num_bytes
        if b >= 1024 ** 3:
            return f"{b / 1024 ** 3:.2f} GB"
        elif b >= 1024 ** 2:
            return f"{b / 1024 ** 2:.2f} MB"
        elif b >= 1024:
            return f"{b / 1024:.2f} KB"
        else:
            return f"{b} B"

    def summary_str(self):
        """
        Returns a human-readable summary string.
        """
        usage = self.bytes_to_str(self.total_usage_bytes)
        limit = self.bytes_to_str(self.device_total_bytes)
        if self.fits_in_memory():
            return f"Total usage {usage} fits within device memory {limit}."
        else:
            over = self.bytes_to_str(self.overflow_bytes())
            return (f"Total usage {usage} exceeds device memory {limit} "
                    f"by {over}.")
