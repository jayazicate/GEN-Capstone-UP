import os
import urllib.parse, urllib.request
import csv

SAVE_LOCATION = 'streetview/' # location to store image at
API_KEY = '&key=' + os.environ.get('STREET_VIEW_API_KEY') # retrieve api key as an environment variable
ADDRESS_FILE = 'mb_final.csv'

def get_street_view(address, save_file_path):
    base = 'https://maps.googleapis.com/maps/api/streetview?size=800x800&location='
    url = base + urllib.parse.quote_plus(address) + API_KEY # added url encoding
    urllib.request.urlretrieve(url, save_file_path)

with open(ADDRESS_FILE) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    next(reader) # skip header line
    i = 0
    for row in reader:
        if i >= 100:
            break
        address = row[31]
        get_street_view(address, SAVE_LOCATION + address + '.jpg')
        i += 1