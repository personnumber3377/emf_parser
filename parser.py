
TEST_FILE_NAME = "DrawString.emf"


from header import * # For parsing the header etc...
import struct

TEST = False

def parse_header(data):
	# EmfMetafileHeaderExtension2
	h, restofdata = read_header(data) # Read the header from the data...
	return h, restofdata

'''

This was taken straight from the spec file...

Type (4 bytes): An unsigned integer that identifies this record type as EMR_BITBLT. This value is
0x0000004C.
Bounds (16 bytes): A RectL object ([MS-WMF] section 2.2.2.19) that specifies the destination
bounding rectangle in logical coordinates. If the intersection of this rectangle with the current
clipping regions (section 3.1.1.2.1) in the playback device context (section 3.1) is empty, this
record has no effect.
xDest (4 bytes): A signed integer that specifies the logical x-coordinate of the upper-left corner of
the destination rectangle.
yDest (4 bytes): A signed integer that specifies the logical y-coordinate of the upper-left corner of
the destination rectangle.
cxDest (4 bytes): A signed integer that specifies the logical width of the source and destination
rectangles.
cyDest (4 bytes): A signed integer that specifies the logical height of the source and destination
rectangles.
BitBltRasterOperation (4 bytes): An unsigned integer that specifies the raster operation code. This
code defines how the color data of the source rectangle is to be combined with the color data of
the destination rectangle and optionally a brush pattern, to achieve the final color.
This value is in the Ternary Raster Operation enumeration ([MS-WMF] section 2.1.1.31).
xSrc (4 bytes): A signed integer that specifies the logical x-coordinate of the upper-left corner of the
source rectangle.
ySrc (4 bytes): A signed integer that specifies the logical y-coordinate of the upper-left corner of the
source rectangle.
XformSrc (24 bytes): An XForm object (section 2.2.28) that specifies a world-space to pagespace transform to apply to the source bitmap.
BkColorSrc (4 bytes): A ColorRef object ([MS-WMF] section 2.2.2.8) that specifies the background
color of the source bitmap.
UsageSrc (4 bytes): An unsigned integer that specifies how to interpret values in the color table in
the source bitmap header. This value is in the DIBColors enumeration (section 2.1.9).
offBmiSrc (4 bytes): An unsigned integer that specifies the offset in bytes, from the start of this
record to the source bitmap header in the BitmapBuffer field.
cbBmiSrc (4 bytes): An unsigned integer that specifies the size in bytes, of the source bitmap
header.
offBitsSrc (4 bytes): An unsigned integer that specifies the offset in bytes, from the start of this
record to the source bitmap bits in the BitmapBuffer field.
cbBitsSrc (4 bytes): An unsigned integer that specifies the size in bytes, of the source bitmap bits.
84 / 282
[MS-EMF] - v20240423
Enhanced Metafile Format
Copyright © 2024 Microsoft Corporation
Release: April 23, 2024
BitmapBuffer (variable): A buffer containing the source bitmap, which is not required to be
contiguous with the fixed portion of the EMR_BITBLT record. Thus, fields in this buffer that are
labeled "UndefinedSpace" are optional and MUST be ignored.


'''

import copy
import struct

def read_bytes(buffer, n): # Cuts first n bytes from buffer. Returns tuple where first element is the cut bytes and second element is the rest of the data.
	return buffer[:n], buffer[n:]

def parse_records(record_data):
	# Returns a list of record objects...
	b = record_data # Keep track of the rest of the data
	while b:
		# Unpack type and length.
		assert len(b) >= 8 # Should be atleast 8 bytes for the type and length.
		t_and_l = b[:8]
		# try to unpack the stuff here
		t, l = struct.unpack('II', t_and_l) # Unpack two little endian integers.
		rec_bytes = b[:l] # Cutoff at l.
		print("Here are the record bytes: "+str(rec_bytes))
		#print(t == 0x0000004C)
		if TEST and t == 0x0000004C: # EMR_BITBLT record
			print("EMR_BITBLT")
			stuff = copy.deepcopy(rec_bytes)
			_, stuff = read_bytes(stuff, 4) # Skip type
			_, stuff = read_bytes(stuff, 4) # Skip length
			bounds, stuff = read_bytes(stuff, 16) # Bounds which is a RectL object.
			xDest, stuff = read_bytes(stuff, 4) # xDest
			yDest, stuff = read_bytes(stuff, 4) # yDest

			cxDest, stuff = read_bytes(stuff, 4) # cxDest
			cyDest, stuff = read_bytes(stuff, 4) # cyDest

			# BitBltRasterOperation
			BitBltRasterOperation, stuff = read_bytes(stuff, 4) # cyDest

			xSrc, stuff = read_bytes(stuff, 4) # xSrc
			ySrc, stuff = read_bytes(stuff, 4) # ySrc

			# XformSrc
			xSrc, stuff = read_bytes(stuff, 24) #  An XForm object (section 2.2.28) that specifies a world-space to pagespace transform to apply to the source bitmap.

			BkColorSrc, stuff = read_bytes(stuff, 4) # BkColorSrc
			# UsageSrc
			UsageSrc, stuff = read_bytes(stuff, 4) # UsageSrc
			offBmiSrc, stuff = read_bytes(stuff, 4) # offBmiSrc

			cbBmiSrc, stuff = read_bytes(stuff, 4) # cbBmiSrc

			offBitsSrc, stuff = read_bytes(stuff, 4) # offBitsSrc
			cbBitsSrc, stuff = read_bytes(stuff, 4) # cbBitsSrc
			#cbBitsSrc, stuff = read_bytes(stuff, 4)
			BitmapBuffer = stuff # This should be rest of the stuff.
			print("BitmapBuffer: "+str(BitmapBuffer))
			BitBltRasterOperation = int.from_bytes(BitBltRasterOperation)# struct.unpack("I", BitBltRasterOperation)
			print("BitBltRasterOperation: "+str(hex(BitBltRasterOperation)))
			print("Done!!!"*100)

		b = b[l:] # Cutoff the thing
	return

def test_parser(): # Parse a known EMF file...
	global TEST
	TEST = True
	fh = open(TEST_FILE_NAME, "rb")
	data = fh.read()
	fh.close()
	# Now parse header...
	h, rest_of_data = parse_header(data)
	# Now try to parse the records
	records = parse_records(rest_of_data) # Try to parse the records from the data.



if __name__=="__main__":
	test_parser()
	exit(0)
