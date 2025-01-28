
import struct

class fake_record_other:
	def __init__(self, bytes_stuff):

		type_and_size = bytes_stuff[:8]
		self.Type, self.Size = struct.unpack('II', type_and_size) # Unpack two little endian integers.
		# self.Type = type
		# self.Size = 8
		restofdata = bytes_stuff[8:]
		# Set the rest of the data
		self.otherdata = restofdata # Show the stuff.
		return

	def serialize(self):
		return struct.pack("I", self.Type) + struct.pack("I", self.Size) + self.otherdata


