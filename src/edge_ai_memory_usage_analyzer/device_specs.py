class DeviceSpecs:
    """
    Represents the memory specifications of an edge device.
    Allows setting and retrieving total memory size and memory type.
    """
    MEMORY_TYPES = [
        'LPDDR4', 'LPDDR4X', 'LPDDR5', 'LPDDR5X', 'DDR4', 'DDR5', 'SRAM', 'Other'
    ]

    def __init__(self, total_memory, memory_type='Other'):
        """
        Args:
            total_memory (str|int|float): Total memory size (e.g., '8GB', 4096*1024*1024)
            memory_type (str): Memory type (e.g., 'LPDDR5X')
        """
        from .input_handler import InputHandler
        self.total_memory_bytes = InputHandler.parse_size(total_memory)
        if not isinstance(memory_type, str):
            raise ValueError("memory_type must be a string")
        mem_type = memory_type.upper()
        if mem_type not in (t.upper() for t in self.MEMORY_TYPES):
            raise ValueError(f"Unknown memory type '{memory_type}'")
        self.memory_type = memory_type

    def get_total_memory_bytes(self):
        """Returns total memory in bytes (int)."""
        return self.total_memory_bytes

    def get_total_memory_str(self):
        """Returns total memory as a human-readable string (e.g., '8.0 GB')."""
        b = self.total_memory_bytes
        if b >= 1024**3:
            return f"{b / 1024**3:.2f} GB"
        elif b >= 1024**2:
            return f"{b / 1024**2:.2f} MB"
        elif b >= 1024:
            return f"{b / 1024:.2f} KB"
        else:
            return f"{b} B"

    def get_memory_type(self):
        """Returns the memory type (str)."""
        return self.memory_type

    def __repr__(self):
        return f"<DeviceSpecs {self.get_total_memory_str()} {self.memory_type}>"
