from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from re import search
from urllib.request import urlretrieve
from urllib.error import HTTPError
import csv

# load data from csv
lic_ids = []
labels = []
addresses = []
csv_data_file = 'id_labels_address.csv'
with open(csv_data_file) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    next(reader)
    for row in reader:
        lic_ids.append(row[0])
        labels.append(row[1])
        addresses.append(row[2])

match_url = 'https.*jpg'

# Use incognito mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

# Load advanced search page of rubmaps
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.rubmaps.ch/advanced-search')

# Enter site
enter_site_button = driver.find_element_by_class_name('entersitenotice_enter')
enter_site_button.click()

for i in range(3405, len(addresses)):
    address = addresses[i]
    save_image = labels[i] + 'rubmaps/' + lic_ids[i] + '.jpg'

    driver.get('https://www.rubmaps.ch/advanced-search')
    select_state = Select(driver.find_elements_by_name('state')[1])
    select_state.select_by_visible_text('Florida')

    enter_address = driver.find_element_by_name('address')
    enter_address.send_keys(address)

    search_button = driver.find_element_by_name('submit')
    search_button.click()

    try:
        image_element = driver.find_element_by_class_name('th-img ').find_element_by_tag_name('img')
        image_url = search(match_url, image_element.get_attribute('style')).group(0)
        urlretrieve(image_url, save_image)
    except (NoSuchElementException, AttributeError, HTTPError) as e:
        print('i:', str(i), ', lic_id:', lic_ids[i], ', label:', labels[i])
