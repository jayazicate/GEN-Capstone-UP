from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import re
import string

directory = sys.argv[1]

for filename in os.listdir(directory):
	if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
		directory_filename = "./" + directory + "/" + filename
		print("Finding" + directory_filename)
		input_photo = str(filename)

		input_photo = input_photo.replace('.jpg', '') or input_photo.replace('.JPG', '')

		output_file = input_photo + ".txt"

		f = open(output_file, "a")

		text = str(((pytesseract.image_to_string(Image.open(directory_filename)))))
		text = text.replace('-\n', '')

		print(text)
		
		f.write(text)

		f.close()


