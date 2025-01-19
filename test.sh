#!/bin/sh
cp ../c_header_thing/thing.py ./cthing.py
cp ../c_header_thing/template.py ./template.py
./parse_c_stuff.sh
python3 header.py

