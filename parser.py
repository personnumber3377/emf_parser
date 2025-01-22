
TEST_FILE_NAME = "DrawString.emf"


# from header import * # For parsing the header etc...
import struct

TEST = False



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

from emf_file import * # For parsing the stuff.



def test_parser(): # Parse a known EMF file...
	global TEST
	TEST = True
	fh = open(TEST_FILE_NAME, "rb")
	data = fh.read()
	fh.close()
	# Now parse header...
	# h, rest_of_data = parse_header(data)
	# Now try to parse the records
	# records = parse_records(rest_of_data) # Try to parse the records from the data.
	emf_obj = parse_emf_file(data)
	print("Serialized bytes: "+str(emf_obj.serialize()))
	return

if __name__=="__main__":
	test_parser()
	exit(0)
