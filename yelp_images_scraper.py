from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import json
import os
import csv

api_key = os.environ.get('YELP_API_KEY')
headers = {'Authorization': 'Bearer %s' % api_key}
categories = ['spas', 'eroticmassage', 'massage', 'massage_therapy', 'beautysvc']

def get_business(businesses):
    for business in businesses:
        biz_id = business['id']
        details_url = 'https://api.yelp.com/v3/businesses/' + biz_id
        req = requests.get(details_url, headers=headers)
        details = json.loads(req.text)
        while 'error' in details:
            req = requests.get(details_url, headers=headers)
            details = json.loads(req.text)
        for category in details['categories']:
            if category['alias'] in categories:
                return(biz_id)
    return None


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

api_url = 'https://api.yelp.com/v3/businesses/matches'

for i in range(313, len(addresses)):
    print(str(i) + '/' + str(len(addresses)))
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
    req = requests.get(api_url, params=params, headers=headers)
    results = json.loads(req.text)
    while 'error' in results:
        req = requests.get(api_url, params=params, headers=headers)
        results = json.loads(req.text)
    if not results['businesses']:        
        print('YNF: ' + str(i) + ', ' + lic_ids[i] + ', ' + labels[i])
        continue

    biz_id = get_business(results['businesses'])
    if biz_id == None:
        print('BNF: ' + str(i) + ', ' + lic_ids[i] + ', ' + labels[i])
        continue

    yelp_url = 'https://www.yelp.com/biz_photos/' + biz_id
    req = requests.get(yelp_url)
    data = req.text
    soup = BeautifulSoup(data, 'html.parser')

    seen_urls = []
    count = 0
    start = 0
    while not req.url in seen_urls:
        seen_urls.append(req.url)
        photo_containers = soup.select('div.photo-box.photo-box--interactive')
        if photo_containers:
            for container in photo_containers:
                save_image = 'yelp_images/' + lic_ids[i] + '_' + str(count) + '.jpg'
                photo = container.find('img')
                if photo != None:
                    photo_url = photo.get('src')
                    urlretrieve(photo_url, save_image)
                count += 1
        else:
            print('PNF: ' + str(i) + ', ' + lic_ids[i] + ', ' + labels[i])
            break

        # if soup.find('span', text='Next', class_='pagination-label responsive-hidden-small pagination-links_anchor') == None:
        #     break
        
        start += 30
        new_url = yelp_url + '?start=' + str(start)
        req = requests.get(new_url)
        data = req.text
        soup = BeautifulSoup(data, 'html.parser')
