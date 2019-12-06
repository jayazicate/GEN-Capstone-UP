from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import re
import string

# get the path of the pdf
pdf = "./buslicense.pdf"

# store all the pages of pdf in a variable
pages = convert_from_path(pdf, 500)

# count to store each of the images 
count = 1
print("Converting pdf to .jpg")
for page in pages:
	filename = pdf.replace('.pdf','') + "page_" + str(count) + ".jpg"
	page.save(filename, 'JPEG')
	count = count + 1


file_limit = count - 1

output_file = pdf + "output.txt"

f = open(output_file, "a")

print("Taking list of .jpg and using image_to_string to get text")
for i in range(1, file_limit + 1):
	filename = pdf.replace('.pdf','') + "page_" + str(i) + ".jpg"

	# pytesseract has an function that recognizes text as a string
	text = str(((pytesseract.image_to_string(Image.open(filename)))))

	text = text.replace('-\n', '')
	f.write(text)


f.close()
