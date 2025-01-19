
TEST_FILE_NAME = "DrawString.emf"


from header import * # For parsing the header etc...


def parse_header(data):
	# EmfMetafileHeaderExtension2
	h = header.read_header(data) # Read the header from the data...
	# 
	

def test_parser(): # Parse a known EMF file...
	fh = open(TEST_FILE_NAME, "rb")
	data = fh.read()
	fh.close()
	# Now parse header...


if __name__=="__main__":
	test_parser()
	exit(0)
