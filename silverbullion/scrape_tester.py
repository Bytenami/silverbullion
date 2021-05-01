#%%
import json
import requests
import os
import logging
import boto3
import datetime as dt
from bs4 import BeautifulSoup

#%%
def get_items_urls(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    list_tiers = soup.find_all(attrs={'class' : "list-tiers"})
    items_urls = [t.find(lambda tag: tag.name =='meta' and tag.get('itemprop') =='url') for t in list_tiers]
    items_urls = [tag.get("content") for tag in items_urls if tag]
    return items_urls


#%%

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

dest_dir = r"/home/rehan/Documents/Python/Projects/bytenami/data"
base_url = "https://www.silverbullion.com.sg"
product_urls = [
    "/Shop/Buy/Silver_Bars",
    "/Shop/Buy/Silver_Coins",
    "/Shop/Buy/Gold_Bars",
    "/Shop/Buy/Gold_Coins",

]

for product in product_urls:
    items_urls = []
    product_type = product.split("/")[-1]
    result_data = ""
    logging.info(f"Scraping {product_type}")
    data = requests.get(base_url + product)
    items_urls += get_items_urls(data.text)
    soup = BeautifulSoup(data.text, 'html.parser')
    pagination = soup.find(class_ = "pagination-container")
    if pagination:
        logging.info(f"Mutiple pages found for {product_type}")
        pages = pagination.find(class_ = "PagedList-skipToNext")
        counter = 1
        while pages:
            counter += 1
            next_page_url = base_url + pages.find("a").get("href")
            logging.info(f"Scraping page {counter}, URL: {next_page_url}")
            data_pg = requests.get(next_page_url)
            items_urls += get_items_urls(data_pg.text)
            soup = BeautifulSoup(data_pg.text, 'html.parser')
            pagination = soup.find(class_ = "pagination-container")
            pages = pagination.find(class_ = "PagedList-skipToNext")
    items_urls = list(set(items_urls))
    logging.info(f"Found {len(items_urls)} items under {product_type}")
    for item in items_urls:
        logging.info(f"Scraping {item}")
        data_item = requests.get(item)
        result_data += data_item.text
    fnam = f"silver_bullion_{product_type.lower()}_{dt.datetime.utcnow()}.html"
    #s3.Object("bn-silverbullion", fnam).put(Body=result_data)
    with open(os.path.join(dest_dir, fnam), "w") as f:
        f.write(result_data)

#TODO
# use <div class="list-tiers"> to get product URLS from each page
# <meta itemprop="url" content=" the get all individual product pages
# join product pages under respective category so only 4 files made


#%%
'''
url = "https://www.silverbullion.com.sg/Shop/Buy/Silver_Bars"
data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')
list_tiers = soup.find_all(attrs={'class' : "list-tiers"})
items_urls = [t.find(lambda tag: tag.name =='meta' and tag.get('itemprop') =='url') for t in list_tiers]
items_urls = [tag.get("content") for tag in items_urls if tag]
'''
