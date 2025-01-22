


import copy
import struct
from header import *
from parser import *
from record_types import * # This is for the names.
# from autogenerated import * # This is for the autogenerated EMF record classes.
import autogenerated

def parse_header(data):
	# EmfMetafileHeaderExtension2
	h, restofdata = read_header(data) # Read the header from the data...
	return h, restofdata

def read_bytes(buffer, n): # Cuts first n bytes from buffer. Returns tuple where first element is the cut bytes and second element is the rest of the data.
	return buffer[:n], buffer[n:]

def lookup_emr_record_class(t): # This returns the class name of the record object which corresponds to record type t.
	return getattr(autogenerated, EMR_NAMES[t]) # autogenerated

def parse_records(record_data):
	# Returns a list of record objects...
	b = record_data # Keep track of the rest of the data
	record_objects = []
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
		c = lookup_emr_record_class(t)
		# Now actually initialize the object.
		rec = c(rec_bytes)
		record_objects.append(rec)
		b = b[l:] # Cutoff the thing
	return record_objects



def get_actual_length(record): # This outputs the actual length of the record.
	return


class EMFFile:
	def __init__(self, h, recs, orig_data): # Initialization function
		self.h = h # Header.
		self.records = recs # Records
		self.mutated = False # Has been mutated?

	def serialize(self): # Serialize data back.
		# First serialize all of the record objects... we can not use orig_data because the object may have been mutated or changed.



		return

def parse_emf_file(data):
	h, rest_of_data = parse_header(data)
	# Now try to parse the records
	records = parse_records(rest_of_data) # Try to parse the records from the data.
	print("Here are the records: "+str(records))
	obj = EMFFile(h, records, copy.deepcopy(data))

	return obj

