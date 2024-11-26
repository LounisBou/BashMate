#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ConvertIt:
    """
    A helper class to convert data types.
    """

    # Define the size units in order with integer sizes
    SIZE_UNIT = {
        'B': 1,
        'KB': 1024,  # 1024 bytes per kilobyte
        'MB': 1024 ** 2,  # 1024 kilobytes per megabyte
        'GB': 1024 ** 3,  # 1024 megabytes per gigabyte
        'TB': 1024 ** 4,  # 1024 gigabytes per terabyte
        'PB': 1024 ** 5,  # 1024 terabytes per petabyte
        'EB': 1024 ** 6,  # 1024 petabytes per exabyte
        'ZB': 1024 ** 7,  # 1024 exabytes per zettabyte
        'YB': 1024 ** 8,  # 1024 zettabytes per yottabyte
    }
    # Define the time units with their durations in milliseconds
    TIME_UNITS = {
        'ms': 1,
        's': 1000,  # 1000 milliseconds per second
        'm': 60 * 1000,  # 60 seconds per minute
        'h': 60 * 60 * 1000,  # 60 minutes per hour
        'd': 24 * 60 * 60 * 1000,  # 24 hours per day
        'w': 7 * 24 * 60 * 60 * 1000,  # 7 days per week
        'mo': 30 * 24 * 60 * 60 * 1000,  # 30 days per month
        'y': 365 * 24 * 60 * 60 * 1000,  # 365 days per year
    }

    @staticmethod
    def size(size: float, current_unit: str = 'B', target_unit: str = None) -> tuple[float, str]:
        """
        Convert the size from the current unit to a target unit.

        Args:
            size (float): Size in the current unit.
            current_unit (str, optional): The unit of the input size. Defaults to 'B'.
            target_unit (str, optional): Target unit to convert to. Defaults to None (automatic).

        Returns:
            tuple[float, str]: Size in the target unit and the unit name.
        """

        if current_unit not in ConvertIt.SIZE_UNIT:
            raise ValueError(f"Invalid current unit: {current_unit}")

        # Convert input size to bytes
        size_in_bytes = size * ConvertIt.SIZE_UNIT[current_unit]

        if target_unit is not None:
            if target_unit not in ConvertIt.SIZE_UNIT:
                raise ValueError(f"Invalid target unit: {target_unit}")
            # Convert bytes to target unit
            size_in_unit = size_in_bytes / ConvertIt.SIZE_UNIT[target_unit]
            return size_in_unit, target_unit
        else:
            # Automatically choose the largest unit
            for unit_name, unit_size in reversed(ConvertIt.SIZE_UNIT.items()):
                if size_in_bytes >= unit_size:
                    size_in_unit = size_in_bytes / unit_size
                    return size_in_unit, unit_name
            # If size is smaller than the smallest unit
            return size_in_bytes, 'B'

    @staticmethod
    def time(time_value: float, current_unit: str = 'ms', target_unit: str = None) -> tuple[float, str]:
        """
        Convert the time from the current unit to a target unit.

        Args:
            time_value (float): Time in the current unit.
            current_unit (str, optional): The unit of the input time. Defaults to 'ms'.
            target_unit (str, optional): Target unit to convert to. Defaults to None (automatic).

        Returns:
            tuple[float, str]: Time in the target unit and the unit name.
        """

        if current_unit not in ConvertIt.TIME_UNITS:
            raise ValueError(f"Invalid current unit: {current_unit}")

        # Convert input time to milliseconds
        time_in_ms = time_value * ConvertIt.TIME_UNITS[current_unit]

        if target_unit is not None:
            if target_unit not in ConvertIt.TIME_UNITS:
                raise ValueError(f"Invalid target unit: {target_unit}")
            # Convert milliseconds to target unit
            time_in_unit = time_in_ms / ConvertIt.TIME_UNITS[target_unit]
            return time_in_unit, target_unit
        else:
            # Automatically choose the largest unit
            for unit_name, unit_ms in reversed(ConvertIt.TIME_UNITS.items()):
                if time_in_ms >= unit_ms:
                    time_in_unit = time_in_ms / unit_ms
                    return time_in_unit, unit_name
            # If time is smaller than the smallest unit
            return time_in_ms, 'ms'

    # Human-readable conversion

    @staticmethod
    def size_human_readable(size: int, current_unit: str = 'B') -> str:
        """
        Convert the size to a human-readable format with multiple units.

        Args:
            size (int): Size in the current unit.
            current_unit (str, optional): The unit of the input size. Defaults to 'B'.

        Returns:
            str: Human-readable size in multiple units.
        """
        # Convert input size to bytes
        if current_unit not in ConvertIt.SIZE_UNIT:
            raise ValueError(f"Invalid current unit: {current_unit}")
        size_in_bytes = size * ConvertIt.SIZE_UNIT[current_unit]
        result_parts = []
        # Get units in descending order
        units = sorted(ConvertIt.SIZE_UNIT.items(), key=lambda x: x[1], reverse=True)
        remaining_size = size_in_bytes
        for unit_name, unit_size in units:
            unit_amount = remaining_size // unit_size
            if unit_amount > 0:
                result_parts.append(f"{int(unit_amount)}{unit_name}")
                remaining_size -= unit_amount * unit_size
        if not result_parts:
            result_parts.append(f"0B")
        return ', '.join(result_parts)

    @staticmethod
    def time_human_readable(time_value: float, current_unit: str = 'ms') -> str:
        """
        Convert the time to a human-readable format with multiple units.

        Args:
            time_value (float): Time in current unit.
            current_unit (str, optional): The unit of the input time. Defaults to 'ms'.

        Returns:
            str: Human-readable time in multiple units.
        """
        if current_unit not in ConvertIt.TIME_UNITS:
            raise ValueError(f"Invalid current unit: {current_unit}")
        time_in_ms = time_value * ConvertIt.TIME_UNITS[current_unit]
        result_parts = []
        # Get units in descending order
        units = sorted(ConvertIt.TIME_UNITS.items(), key=lambda x: x[1], reverse=True)
        remaining_time = time_in_ms
        for unit_name, unit_ms in units:
            unit_amount = remaining_time // unit_ms
            if unit_amount > 0:
                result_parts.append(f"{int(unit_amount)}{unit_name}")
                remaining_time -= unit_amount * unit_ms
        if not result_parts:
            result_parts.append(f"0ms")
        return ', '.join(result_parts)

# Main function to test the helper class
if __name__ == '__main__':

    # Test the human-readable size conversion
    print(f"\nTest of human-readable size conversion:")
    size_human_readable_tests = {
        '5TB, 4GB, 3MB, 2KB, 1B': 5 * 1024 ** 4 + 4 * 1024 ** 3 + 3 * 1024 ** 2 + 2 * 1024 + 1,
    }
    for size_str, size in size_human_readable_tests.items():
        result = ConvertIt.size_human_readable(size)
        print(f"Expected: {size_str}")
        print(f"Result:   {result}")

    # Test the human-readable time conversion
    print(f"\nTest of human-readable time conversion:")
    time_human_readable_tests = {
        '5y, 4mo, 3w, 2d, 1h, 30m, 20s, 10ms':
            (5 * 365 * 24 * 60 * 60 * 1000)
            + (4 * 30 * 24 * 60 * 60 * 1000)
            + (3 * 7 * 24 * 60 * 60 * 1000)
            + (2 * 24 * 60 * 60 * 1000)
            + (1 * 60 * 60 * 1000)
            + (30 * 60 * 1000)
            + (20 * 1000)
            + 10,
    }
    for time_str, time_value in time_human_readable_tests.items():
        result = ConvertIt.time_human_readable(time_value)
        print(f"Expected: {time_str}")
        print(f"Result:   {result}")
