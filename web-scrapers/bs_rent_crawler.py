import csv
import time
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

        houses_data.append({'title': title, 'location': location, 'size': size, 'rental fee': price})


# Save the data to a CSV file
csv_file_path = './data/houses-for-rent.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
    csv_writer = csv.DictWriter(f, fieldnames=['title', 'location', 'size', 'rental fee'])
    csv_writer.writeheader()
    csv_writer.writerows(houses_data)

 # Record the end time
end_time = time.time()
 # Calculate the time taken 
elapsed_time = end_time - start_time 

print("Data saved in houses-for-rent.csv file successfully")
print(f"Time taken to download the data: {elapsed_time:.2f} seconds")