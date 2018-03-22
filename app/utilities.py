import datetime
import struct
import time


def current_timestamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S'), ts


def dataConv(data1, data2):
    value = data1 | (data2 << 8)
    if value & (1 << 16 - 1):
        value -= (1 << 16)
    return value


def unpack_signed_20bit(msb, lsb, xlsb):
    binary_string_literal = "{:08b}".format(msb) + "{:08b}".format(lsb) + "{:08b}".format(xlsb)[0:4]
    binary_data = int(binary_string_literal, 2)
    four_bytes = bytes.fromhex("{:08x}".format(binary_data))
    value = struct.unpack(">i", four_bytes)[0]
    return value


def unpack_unsigned(msb, lsb):
    binary_string_literal = "{:08b}".format(msb) + "{:08b}".format(lsb)
    binary_data = int(binary_string_literal, 2)
    two_bytes = bytes.fromhex("{:08x}".format(binary_data))
    value = struct.unpack(">I", two_bytes)[0]
    return value


def unpack_signed(msb, lsb):
    binary_string_literal = "{:08b}".format(msb) + "{:08b}".format(lsb)
    binary_data = int(binary_string_literal, 2)
    two_bytes = bytes.fromhex("{:08x}".format(binary_data))
    value = struct.unpack(">i", two_bytes)[0]
    return value


def unpack_unsigned_short(msb, lsb):
    binary_string_literal = "{:08b}".format(msb) + "{:08b}".format(lsb)
    binary_data = int(binary_string_literal, 2)
    two_bytes = bytes.fromhex("{:04x}".format(binary_data))
    value = struct.unpack(">H", two_bytes)[0]
    return value


def unpack_signed_short(msb, lsb):
    binary_string_literal = "{:08b}".format(msb) + "{:08b}".format(lsb)
    binary_data = int(binary_string_literal, 2)
    two_bytes = bytes.fromhex("{:04x}".format(binary_data))
    value = struct.unpack(">h", two_bytes)[0]
    return value
