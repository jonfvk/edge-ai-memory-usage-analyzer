class InputHandler:
    """
    Handles input for model and input data sizes.
    Accepts sizes in bytes, kilobytes, megabytes, or gigabytes.
    """
    SIZE_UNITS = {
        'b': 1,
        'kb': 1024,
        'mb': 1024 ** 2,
        'gb': 1024 ** 3
    }

    @staticmethod
    def parse_size(size_str):
        """
        Parse a size string like '128MB', '2 gb', '512kb', or '1048576'.
        Returns the size in bytes as an integer.
        Raises ValueError on invalid input.
        """
        if isinstance(size_str, (int, float)):
            if size_str < 0:
                raise ValueError("Size must be non-negative")
            return int(size_str)
        if not isinstance(size_str, str):
            raise ValueError("Size must be a string or number")
        s = size_str.strip().lower().replace(' ', '')
        num = ''
        unit = ''
        for c in s:
            if c.isdigit() or c == '.':
                num += c
            else:
                unit += c
        if not num:
            raise ValueError(f"No numeric value found in '{size_str}'")
        value = float(num)
        if not unit:
            # Default to bytes
            return int(value)
        if unit not in InputHandler.SIZE_UNITS:
            raise ValueError(f"Unknown size unit '{unit}' in '{size_str}'")
        return int(value * InputHandler.SIZE_UNITS[unit])

    def get_model_and_data_size(self, model_size, input_data_size):
        """
        Accepts model and input data sizes (as strings or numbers).
        Returns a tuple: (model_size_bytes, input_data_size_bytes)
        """
        model_bytes = self.parse_size(model_size)
        data_bytes = self.parse_size(input_data_size)
        return model_bytes, data_bytes
