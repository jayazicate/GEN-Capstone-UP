from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import json
import os
import csv

# load data from csv
lic_ids = []
labels = []
addresses = []
csv_data_file = 'address_id_label.csv'
with open(csv_data_file) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    next(reader)
    for row in reader:
        addresses.append(row[0])
        lic_ids.append(row[1])
        labels.append(row[2])

api_key = os.environ.get('YELP_API_KEY')

headers = {'Authorization': 'Bearer %s' % api_key}
url = 'https://api.yelp.com/v3/businesses/matches'

for i in range(len(addresses)):
    if i >= 10:
        break
    split_address = addresses[i].split(', ')
    address1 = split_address[0]
    city = split_address[1]
    zip_code = split_address[2][3:]

    params = {
        'name': '',
        'address1': address1,
        'city': city,
        'state': 'FL',
        'country': 'US',
        'zip_code': zip_code,
        'match_threshold': 'none'
    }
    req = requests.get(url, params=params, headers=headers)

    results = json.loads(req.text)
    if not results['businesses']:        
        print('YNF: ' + str(i) + ', ' + lic_ids[i] + ', ' + labels[i])
        continue

    biz_id = results['businesses'][0]['id']
    print(addresses[i] + ': ' + biz_id)

    url = 'https://www.yelp.com/biz_photos/' + biz_id
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, 'html.parser')

    seen_urls = []
    count = 0
    start = 0
    while not req.url in seen_urls:
        seen_urls.append(req.url)
        photo_containers = soup.select('div.photo-box.photo-box--interactive')
        if photo_containers != None:
            for container in photo_containers:
                save_image = 'yelp_images/' + lic_ids[i] + '_' + str(count) + '.jpg'
                photo = container.find('img')
                if photo != None:
                    photo_url = photo.get('src')
                    urlretrieve(photo_url, save_image)
                count += 1
        else:
            print('PNF: ' + str(i) + ', ' + lic_ids[i] + ', ' + labels[i])

        # if soup.find('span', text='Next', class_='pagination-label responsive-hidden-small pagination-links_anchor') == None:
        #     break
        
        start += 30
        url = 'https://www.yelp.com/biz_photos/west-wind-automotive-san-francisco-2?start=' + str(start)
        req = requests.get(url)
        data = req.text
        soup = BeautifulSoup(data, 'html.parser')
