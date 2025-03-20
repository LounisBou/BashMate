#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class ULID:
    """
    A Universally Unique Lexicographically Sortable Identifier (ULID) is a 128-bit
    identifier that is represented as a 26-character string. The first 10 characters
    are a timestamp, and the last 16 characters are random.
    """
    ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    ENCODING_LENGTH = len(ENCODING)
    TIME_LENGTH = 10
    RANDOM_LENGTH = 16
    TOTAL_LENGTH = TIME_LENGTH + RANDOM_LENGTH

    def __init__(self, ulid_string: str, format_hint=None):
        """
        Create a new ULID instance.
        ---
        Parameters:
        - ulid_string (str): The ULID string to convert.
        - format_hint (str, optional): Hint about the format (mysql_binary, hex, base32).
        """
        # Check if it's a MySQL hex literal format (X'...')
        mysql_hex_match = re.match(r"^X'([0-9A-Fa-f]+)'$", ulid_string)
        if mysql_hex_match:
            print("Provided ULID is in MySQL hex literal format")
            self.binary = bytes.fromhex(mysql_hex_match.group(1))
        # Check if it's a 0x prefixed hex string
        elif ulid_string.startswith('0x'):
            print("Provided ULID is a 0x-prefixed hexadecimal string")
            self.binary = bytes.fromhex(ulid_string[2:])
        # Check ULID string type
        elif format_hint == 'base32' or self.is_base32_string(ulid_string):
            print("Provided ULID is a base32 string")
            self.binary = self.base32_to_binary(ulid_string)
        elif format_hint == 'hex' or self.is_hex_string(ulid_string):
            print("Provided ULID is a hexadecimal string")
            self.binary = bytes.fromhex(ulid_string)
        else:
            print("Provided ULID is treated as a binary string")
            # Convert the binary string to bytes
            self.binary = ulid_string.encode('latin-1')
            
            # Print out the bytes for diagnosis
            byte_array = list(self.binary)
            print(f"Binary ULID bytes ({len(byte_array)}): {byte_array}")

        # Handle binary length
        binary_len = len(self.binary)
        if binary_len != 16:
            if binary_len == 15:
                # Special case for MySQL binary ULIDs which often are missing the first byte
                print(f"Detected MySQL binary ULID format (15 bytes), prepending '01' byte")
                self.binary = b'\x01' + self.binary
            elif binary_len < 16:
                # Pad the binary if too short
                print(f"Binary length is {binary_len} bytes, padding to 16 bytes.")
                self.binary = self.binary.rjust(16, b'\x00')  # Prepend zeros instead of appending
            else:
                # Truncate if too long
                print(f"Binary length is {binary_len} bytes, truncating to 16 bytes.")
                self.binary = self.binary[:16]

        # Convert the ULID to various formats
        self.hex = self.binary_to_hex(self.binary)
        self.base32 = self.binary_to_base32(self.binary)

    def __str__(self) -> str:
        """
        Return all forms of the ULID
        """
        binary_bytes = list(self.binary)
        return f"""
        Binary bytes: {binary_bytes}
        Binary (raw): {self.binary}
        Hexadecimal: {self.hex}
        Base32: {self.base32}
        MySQL Hex: X'{self.hex}'
        UUID: {self.binary_to_uuid(self.binary)}
        Datetime: {self.binary_to_datetime(self.binary)}
        Timestamp: {self.binary_to_timestamp(self.binary)}
        """

    def __repr__(self) -> str:
        """
        Return a string representation of the ULID instance.
        """
        return f"ULID({self.binary})"

    def __eq__(self, other):
        """
        Check if two ULID instances are equal.

        Args:
            other (ULID): The other ULID instance to compare.

        Returns:
            bool: True if the ULIDs are equal, False otherwise.
        """
        return self.binary == other.binary

    def __ne__(self, other):
        """
        Check if two ULID instances are not equal.

        Args:
            other (ULID): The other ULID instance to compare.

        Returns:
            bool: True if the ULIDs are not equal, False otherwise.
        """
        return self.binary != other.binary

    def __lt__(self, other):
        """
        Check if this ULID instance is less than another based on datetime.
        This is useful for sorting ULIDs.

        Args:
            other (ULID): The other ULID instance to compare.

        Returns:
            bool: True if this ULID is less than the other, False otherwise.
        """
        return self.binary_to_datetime(self.binary) < self.binary_to_datetime(other.binary)

    def __le__(self, other):
        """
        Check if this ULID instance is less than or equal to another based on datetime.

        Args:
            other (ULID): The other ULID instance to compare.

        Returns:
            bool: True if this ULID is less than or equal to the other, False otherwise.
        """
        return self.binary_to_datetime(self.binary) <= self.binary_to_datetime(other.binary)

    def __gt__(self, other):
        """
        Check if this ULID instance is greater than another based on datetime.

        Args:
            other (ULID): The other ULID instance to compare.

        Returns:
            bool: True if this ULID is greater than the other, False otherwise.
        """
        return self.binary_to_datetime(self.binary) > self.binary_to_datetime(other.binary)
 
    def __ge__(self, other):
        """
        Check if this ULID instance is greater than or equal to another based on datetime.

        Args:
            other (ULID): The other ULID instance to compare.

        Returns:
            bool: True if this ULID is greater than or equal to the other, False otherwise.
        """
        return self.binary_to_datetime(self.binary) >= self.binary_to_datetime(other.binary)

    def __hash__(self):
        """
        Return the hash of the ULID instance.

        Returns:
            int: The hash of the ULID instance.
        """
        return hash(self.binary)

    def __len__(self):
        """
        Return the length of the ULID instance.

        Returns:
            int: The length of the ULID instance.
        """
        return len(self.binary)

    @staticmethod
    def is_hex_string(s: str) -> bool:
        """
        Check if a string is a valid hexadecimal string

        Args:
        - s (str): The string to check.

        Returns:
        - bool: True if the string is a valid hexadecimal string, False otherwise.
        """
        return bool(re.match(r'^[0-9A-Fa-f]+$', s))

    @classmethod
    def is_base32_string(cls, s: str) -> bool:
        """
        Check if a string is a valid base32 string

        Args:
        - s (str): The string to check.

        Returns:
        - bool: True if the string is a valid base32 string, False otherwise.
        """
        if len(s) != cls.TOTAL_LENGTH:
            return False
        return all(c in cls.ENCODING for c in s.upper())

    @classmethod
    def base32_to_binary(cls, base32_str):
        """
        Convert a base32 ULID to a binary string.

        Args:
            base32_str (str): The base32 ULID string.

        Returns:
            bytes: The converted binary string.
        """
        # Normalize to uppercase
        base32_str = base32_str.upper()
        
        # Check if the string is a valid base32 string
        if len(base32_str) != cls.TOTAL_LENGTH:
            raise ValueError(f"Invalid ULID length: {len(base32_str)}")

        # Create a reverse lookup dictionary
        decode_map = {char: index for index, char in enumerate(cls.ENCODING)}

        # Convert base32 to integer
        val = 0
        for char in base32_str:
            if char not in decode_map:
                raise ValueError(f"Invalid character in ULID: {char}")
            val = (val * cls.ENCODING_LENGTH) + decode_map[char]

        # Convert integer to 16 bytes
        binary = val.to_bytes(16, byteorder='big')

        # Return the binary string
        return binary

    @classmethod
    def binary_to_hex(cls, binary):
        """
        Convert a binary string to a hexadecimal ULID.

        Args:
            binary (bytes): The binary string.

        Returns:
            str: The converted hexadecimal ULID.
        """
        # Convert bytes to hex
        return binary.hex().upper()

    @classmethod
    def binary_to_base32(cls, binary):
        """
        Convert a binary string to a base32 ULID.

        Args:
            binary (bytes): The binary string.

        Returns:
            str: The converted base32 ULID.
        """
        # Convert bytes to integer
        val = int.from_bytes(binary, byteorder='big')

        # Convert integer to base32
        base32_str = ""
        for _ in range(cls.TOTAL_LENGTH):
            val, rem = divmod(val, cls.ENCODING_LENGTH)
            base32_str = cls.ENCODING[rem] + base32_str

        return base32_str

    @classmethod
    def binary_to_uuid(cls, binary):
        """
        Convert a binary string to a UUID.

        Args:
            binary (bytes): The binary string.

        Returns:
            UUID: The converted UUID.
        """
        # Convert bytes to UUID
        return UUID(bytes=binary)

    @classmethod
    def binary_to_datetime(cls, binary):
        """
        Convert a binary string to a datetime object.

        Args:
            binary (bytes): The binary string.

        Returns:
            datetime: The converted datetime object.
        """
        # Convert bytes to integer
        val = int.from_bytes(binary[:6], byteorder='big')

        # Convert integer to datetime
        return datetime.fromtimestamp(val / 1000.0)

    @classmethod
    def binary_to_timestamp(cls, binary):
        """
        Convert a binary string to a timestamp.

        Args:
            binary (bytes): The binary string.

        Returns:
            int: The converted timestamp.
        """
        # Convert bytes to integer
        val = int.from_bytes(binary[:6], byteorder='big')

        # Return the timestamp
        return val // 1000


def main():
    """
    Take an ULID in binary or hexadecimal or base32 format.
    Convert it to binary and hexadecimal and base32 format.
    """

    # Check for format hint argument
    format_hint = None
    if len(sys.argv) >= 3 and sys.argv[1] == '--format':
        format_hint = sys.argv[2]
        ulid_string = sys.argv[3] if len(sys.argv) >= 4 else ""
    elif len(sys.argv) == 2:
        ulid_string = sys.argv[1]
    else:
        print("Usage: python ulidconverter.py [--format {mysql_binary|hex|base32}] <ulid>")
        print("Examples:")
        print("  python ulidconverter.py 01FMMHN4SJDWY420W3THWN5KN2")
        print("  python ulidconverter.py 019109544A6F85CB067E041B598E7A2D")
        print("  python ulidconverter.py 0x019109544A6F85CB067E041B598E7A2D")
        print("  python ulidconverter.py X'019109544A6F85CB067E041B598E7A2D'")
        print("  python ulidconverter.py \"\\tTJoË~Yz-\"")
        print("  python ulidconverter.py --format mysql_binary \"\\tTJoË~Yz-\"")
        sys.exit(1)

    try:
        # Create a new ULID instance
        ulid = ULID(ulid_string, format_hint)
        # Print the ULID in all formats
        print(ulid)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the main function
    main()