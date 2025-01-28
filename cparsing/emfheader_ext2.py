import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '16b', '4b', '4b', '4b', '4b', '2b', '2b', '4b', '4b', '4b', '8b', '8b', '4b', '4b', '4b', '8b']
    remaining_data = b""
    def __init__(self, data):
        unpacked = []
        size_thing = 0
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
            size_thing += struct.calcsize(f) # Add the thing
        fields = ['iType', 'nSize', 'rclBounds', 'rclFrame', 'dSignature', 'nVersion', 'nBytes', 'nRecords', 'nHandles', 'sReserved', 'nDescription', 'offDescription', 'nPalEntries', 'szlDevice', 'szlMillimeters', 'cbPixelFormat', 'offPixelFormat', 'bOpenGL', 'szlMicrometers']
        for field, value in zip(fields, unpacked):
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        # self.remaining_data = data[struct.calcsize("".join(self.format)):]
        #print("poopoooo")
        #print("struct.calcsize(f) == "+str(size_thing))
        #print("self.nSize[1] == "+str(self.nSize[1]))
        self.remaining_data = data[:self.nSize[1]-size_thing]

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['iType', 'nSize', 'rclBounds', 'rclFrame', 'dSignature', 'nVersion', 'nBytes', 'nRecords', 'nHandles', 'sReserved', 'nDescription', 'offDescription', 'nPalEntries', 'szlDevice', 'szlMillimeters', 'cbPixelFormat', 'offPixelFormat', 'bOpenGL', 'szlMicrometers']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['iType', 'nSize', 'rclBounds', 'rclFrame', 'dSignature', 'nVersion', 'nBytes', 'nRecords', 'nHandles', 'sReserved', 'nDescription', 'offDescription', 'nPalEntries', 'szlDevice', 'szlMillimeters', 'cbPixelFormat', 'offPixelFormat', 'bOpenGL', 'szlMicrometers'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out + self.remaining_data # Return the output bytes

