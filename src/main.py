#! .\im_venv\scripts\python.exe

import warnings
warnings.filterwarnings("ignore")

from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tqdm import tqdm
from time import localtime, sleep, strftime


# var declarations
df = pd.DataFrame(columns=['Type', 'Rooms', 'Size', 'Location', 'Price', 'Region'])

type_list = []
rooms_list = []
size_list = []
location_list = []
price_list = []
region_loc_list = []

regions_list = ["ile-de-france", "pays-de-la-loire", "nouvelle-aquitaine", "provence-alpes-cote-d-azur"]

# display local time
start_time = strftime("%H:%M:%S", localtime())
print(start_time)

# Open website
browser = webdriver.Chrome()

# Region choice
for region in range(0,4):
# for i in tqdm(range(0,4), desc='Total progress'):  
#  
    url_reg = f'https://www.orpi.com/recherche/buy?transaction=buy&resultUrl=&locations%5B0%5D%5Bvalue%5D={regions_list[region]}&agency=&minSurface=40&maxSurface=&minLotSurface=&maxLotSurface=&minStoryLocation=&maxStoryLocation=&newBuild=&oldBuild=&minPrice=&maxPrice=&sort=date-down&layoutType=list&page'

    # Scrap data from the 30 first pages of the website
    for page in range(2):

        url = f'{url_reg}={page}' 

        browser.get(url)

        # get all page data
        soup = BeautifulSoup(browser.page_source, 'html.parser')


        all_items = soup.find_all('div', attrs={'class':'c-box__inner c-box__inner--sm c-overlay'})

        
        for item in all_items:

            region_loc_list.append(regions_list[region])

            item_type = item.find('a').find(text=True, recursive=False).strip()
            type_list.append(item_type)

            item_rooms = item.find("span").find("b").find(recursive=False).get_text()
            rooms_list.append(item_rooms)

            # In case there is no size specified
            try:
                item_space = item.select("span b")[2].get_text(strip=True)
                size_list.append(item_space)

            except IndexError:
                size_list.append("No info")

            item_price = item.find("strong", "u-text-md u-color-primary").get_text()
            item_price = item_price.replace("€","").strip()
            price_list.append(item_price)

            item_location = item.find("p", "u-mt-sm").get_text()
            location_list.append(item_location)

    # time.sleep(randint(2,10)) # crawling in short random bursts of time/avoid ip ban

# Storing all data in the dataset
df['Type'] = type_list
df['Rooms'] = rooms_list
df['Size'] = size_list
df['Price'] = price_list
df['Location'] = location_list
df['Region'] = region_loc_list

# Final insights
print(df.iloc[:5])
print("\n")
print(len(df), "items have been scraped.")
print("\n")
print(df.shape)

# storing the dataframe as a CSV file
df.to_csv('./datasets/real_estate_paris_orpi_df.csv', index=False, encoding='utf-8')


# TODO :
#   Scrap from multiple regions (website filter) + créer nouvelle variable dans le tableau pour la region : optimiser path name de recherche classe + verifier m² > 1000 séparateur
#   Get more characteristics/info from house description page
#   pip freeze
#   PowerBI Analysis and push to github


# https://www.orpi.com/recherche/buy?locations%5B0%5D%5Bvalue%5D=ile-de-france&locations%5B0%5D%5Blabel%5D=Ile-de-France%20-%20R%C3%A9gion&sort=date-down&layoutType=mixte&recentlySold=false

# https://www.orpi.com/recherche/buy?locations%5B0%5D%5Bvalue%5D=pays-de-la-loire&locations%5B0%5D%5Blabel%5D=Pays%20de%20la%20Loire%20-%20R%C3%A9gion&sort=date-down&layoutType=mixte&recentlySold=false

