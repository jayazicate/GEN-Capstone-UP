import sys
import string
import os
import re

if len(sys.argv) == 1:
    sys.exit("Empty argument")

# characters we want to filter out
unwanted_chars = [';', '@', '!', '/']

# get text file and convert it to string
text_file = sys.argv[1]
f = open(text_file, "r");
string = f.read()

print("Old String:")
print(string)

f.close()

for i in unwanted_chars:
    string = string.replace(i, '')
    
print("New String:")
print(string)
    
new_output_file = "filtered_" + text_file

nf = open(new_output_file, "a")
nf.write(string)
nf.close()