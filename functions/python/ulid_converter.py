#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
import binascii
from datetime import datetime

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

    @classmethod
    def decode_base32(cls, string: str) -> bytes:
        """
        Convert a base32 string to bytes.
        ---
        Parameters:
        - string: A base32 string.
        Returns:
        - bytes: The decoded bytes.
        """
        if len(string) != cls.TOTAL_LENGTH:
            raise ValueError(f"Invalid ULID length: {len(string)}")

        # Create a reverse lookup dictionary
        decode_map = {char: index for index, char in enumerate(cls.ENCODING)}
        
        # Convert base32 to integer
        val = 0
        for char in string:
            if char not in decode_map:
                raise ValueError(f"Invalid character in ULID: {char}")
            val = (val * cls.ENCODING_LENGTH) + decode_map[char]
        
        # Convert integer to 16 bytes
        return val.to_bytes(16, byteorder='big')

    @classmethod
    def from_string(cls, base32_str: str) -> 'ULID':
        """
        Create a ULID instance from a base32 string.
        ---
        Parameters:
        - base32_str: A base32 string.
        Returns:
        - ULID: The ULID instance.
        """
        binary = cls.decode_base32(base32_str)
        return cls(binary)

    def __init__(self, binary: bytes):
        """
        Create a new ULID instance.
        ---
        Parameters:
        - binary: A 16-byte binary string.
        """
        if len(binary) != 16:
            raise ValueError("Binary ULID must be exactly 16 bytes")
        self.binary = binary

    def __str__(self) -> str:
        """
        Return the base32 string representation.
        ---
        Returns:
        - str: The base32 string.
        """
        # Convert bytes to integer
        val = int.from_bytes(self.binary, byteorder='big')
        
        # Convert to base32
        string = ""
        for _ in range(self.TOTAL_LENGTH):
            val, mod = divmod(val, self.ENCODING_LENGTH)
            string = self.ENCODING[mod] + string
        return string

    def to_binary(self) -> bytes:
        """
        Return the binary representation.
        ---
        Returns:
        - bytes: The 16-byte binary
        """
        return self.binary

def main():
    """
    Convert a base32 ULID to hexadecimal.
    """

    # Check if the base32 ULID is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <base32-ulid>")
        sys.exit(1)
    # Convert the base32 ULID to hexadecimal
    base32_ulid = sys.argv[1]
    try:
        ulid = ULID.from_string(base32_ulid)
        result = {
            'base32': str(ulid),
            'hexadecimal': '0x' + binascii.hexlify(ulid.to_binary()).decode('ascii')
        }
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    """
    Run the main function.
    """
    main()