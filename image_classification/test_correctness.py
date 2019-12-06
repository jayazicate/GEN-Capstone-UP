import csv
import os
import re

labels_dict = {}
with open('mb_final_refined3.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    next(reader)
    for row in reader:
        labels_dict[row[45]] = row[47]

images_0 = os.listdir('perfect0')
for image_name in images_0:
    lic_id = re.match('[0-9]+', image_name).group(0)
    if float(labels_dict[lic_id]) > 0:
        print('lic_id:', lic_id, ', label:', labels_dict[lic_id])

print('-----------------')

images_1 = os.listdir('perfect1')
for image_name in images_1:
    lic_id = re.match('[0-9]+', image_name).group(0)
    if float(labels_dict[lic_id]) < 0.8:
        print('lic_id:', lic_id, ', label:', labels_dict[lic_id])