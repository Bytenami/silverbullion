#%%
import json
import requests
import os
import boto3
import datetime as dt
from bs4 import BeautifulSoup

dest_dir = r"/home/rehan/Documents/Python/Projects/bytenami/data"
base_url = "https://www.silverbullion.com.sg"
product_urls = [
    "/Shop/Buy/Silver_Bars",
    "/Shop/Buy/Silver_Coins",
    "/Shop/Buy/Gold_Bars",
    "/Shop/Buy/Gold_Coins",

]

for product in product_urls:
    page_no = 1
    product_type = product.split("/")[-1]
    url_data = {}
    data = requests.get(base_url + product)
    url_data[page_no] = data.text
    soup = BeautifulSoup(data.text, 'html.parser')
    pagination = soup.find(class_ = "pagination-container")
    if pagination:
        pages = pagination.find(class_ = "PagedList-skipToNext")
        while pages:
            page_no += 1
            next_page_url = base_url + pages.find("a").get("href")
            data_pg = requests.get(next_page_url)
            url_data[page_no] = data_pg.text
            soup = BeautifulSoup(data_pg.text, 'html.parser')
            pagination = soup.find(class_ = "pagination-container")
            pages = pagination.find(class_ = "PagedList-skipToNext")
    for k, v in url_data.items():
        fnam = f"silver_bullion_{product_type.lower()}_{k}_{dt.datetime.utcnow()}.html"
        #s3.Object("bn-silverbullion", fnam).put(Body=v)
        with open(os.path.join(dest_dir, fnam), "w") as f:
            f.write(v)

#TODO
# use <div class="list-tiers"> to get product URLS from each page
# <meta itemprop="url" content=" the get all individual product pages
# join product pages under respective category so only 4 files made


#%%
fnam = f"silver_bullion_gold_{dt.datetime.now()}.html"
s3.Object("bn-silverbullion", fnam).put(Body=data.text)
return {"statusCode": 200, "body": len(data.text)}