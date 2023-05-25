import csv
import json
import requests
from bs4 import BeautifulSoup

url_base = 'https://www.buyrentkenya.com/houses-for-rent?page='
headers = {'User-Agent': 'Mozilla/5.0'}


houses_data = []


for page in range(1, 125):
    url = url_base + str(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    listings = soup.find_all('div', class_='px-5') 


    for listing in listings:
        title = listing.find('span', class_='hidden').text.strip()
        location = listing.find('p', class_='text-sm').text.strip()
        size = listing.find('a', class_='text-grey-500').text.strip() 
        price = listing.find('div', {'class': 'flex justify-between items-center'}).text.strip()

        houses_data.append({'title': title, 'location': location, 'size': size, 'price': price})


# print(houses_data)

# Save the data to a JSON file
with open('./data/houses-for-rent.json', 'w') as f:
    json.dump(houses_data, f) 


print("Data saved in houses-for-rent.json file successfully")