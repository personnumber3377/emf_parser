import struct

d = b"\xff"*16

integer = struct.unpack("16b", d)
print(integer)

