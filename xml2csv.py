from xml.etree import ElementTree
import csv
import os

XML_DIRECTORY = 'orig_labels'

with open ('annotate.csv', mode='w') as annotate_file:
    writer = csv.writer(annotate_file, delimiter=',')
    writer.writerow(['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])

    all_files = os.listdir(XML_DIRECTORY)
    all_files.sort()
    for filename in all_files:
        if filename == '.DS_Store':
            continue
        tree = ElementTree.parse(XML_DIRECTORY + '/' + filename)
        root = tree.getroot()

        picture_name = root.find('filename').text
        picture_width = root.find('size').find('width').text
        picture_height = root.find('size').find('height').text
        for obj in root.findall('object'):
            xmin = obj.find('bndbox').find('xmin').text
            ymin = obj.find('bndbox').find('ymin').text
            xmax = obj.find('bndbox').find('xmax').text
            ymax = obj.find('bndbox').find('ymax').text
            class_name = obj.find('name').text

            writer.writerow([picture_name, picture_width, picture_height, class_name, xmin, ymin, xmax, ymax])
