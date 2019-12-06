from bs4 import BeautifulSoup
import requests
import json
import os

api_key = os.environ.get('YELP_API_KEY')

headers = {'Authorization': 'Bearer %s' % api_key}

api_url = 'https://api.yelp.com/v3/businesses/matches'

params = {
    'name': '',
    'address1': '918 Powerline Rd',
    'address2': '',
    'city': 'Pompano Beach',
    'state': 'FL',
    'country': 'US',
    'zip_code': '33069',
    'match_threshold': 'none'
}
req = requests.get(api_url, params=params, headers=headers)

results = json.loads(req.text)
print(results)

# api_url = 'https://api.yelp.com/v3/businesses/search'

# params = {
#     'location': '1419 10th St, Lake Park, FL 33403, USA',
#     'categories': 'spas, eroticmassage, massage, massage_therapy, massage_school',
# }

# req = requests.get(api_url, params=params, headers=headers)

# results = json.loads(req.text)
# print(results)

# api_url = 'https://api.yelp.com/v3/businesses/t0qwfH5n3HuKo4HV5vdf2w'

# req = requests.get(api_url, headers=headers)

# results = json.loads(req.text)
# print(results)