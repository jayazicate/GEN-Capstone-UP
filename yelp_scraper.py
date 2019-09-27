from bs4 import BeautifulSoup
import requests
import csv

URL = 'https://www.yelp.com/biz/asula-wellness-center-portland' # a yelp page
request = requests.get(URL) # load data from yelp page
data = request.text # get raw html text from yelp page
soup = BeautifulSoup(data, 'html.parser') # initialize parse with html content

all_reviews = []
all_reviews_data = soup.find_all('div', class_='review-content') # find all yelp reviews on page
for review_content in all_reviews_data:
    review = []
    review_text = review_content.find('p').text # extract raw text from review
    review.append(review_text)
    review_rating = review_content.find('div', class_='i-stars').get('title') # extract review rating from review
    review.append(review_rating)
    review_date = review_content.find('span', class_='rating-qualifier').text.strip() # extract date that the review was written
    review.append(review_date)
    all_reviews.append(review)

# create a new csv file with reviews
with open('reviews.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Review', 'Rating', 'Date'])
    for review in all_reviews:
        filewriter.writerow([review[0], review[1], review[2]]) # insert all reviews into a csv file

