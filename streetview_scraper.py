import os, urllib.parse, urllib.request

SAVE_LOCATION = r"/Users/adammercer/Desktop" # location on computer to store image at
API_KEY = '&key=' + os.environ.get('STREET_VIEW_API_KEY') # retrieve api key as an environment variable
TEST_ADDRESS = '820 W 7TH AVE, SPOKANE, WA, 99204, UNITED STATES' # a massage parlor in Washington

def getStreetView(address, saveLocation):
    base = 'https://maps.googleapis.com/maps/api/streetview?size=800x800&location='
    url = base + urllib.parse.quote_plus(address) + API_KEY # added url encoding
    fi = address + '.jpg' # save file name
    urllib.request.urlretrieve(url, os.path.join(saveLocation, fi))

getStreetView(TEST_ADDRESS, SAVE_LOCATION)