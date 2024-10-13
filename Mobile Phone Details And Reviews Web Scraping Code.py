#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup


# In[2]:


Header =({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})


# In[8]:


brands = ['Apple','SAMSUNG','Google','MOTOROLA','vivo','OPPO','Infinix','Nothing','POCO','realme','REDMI','ASUS','IQOO','OnePlus','Honor','Micromax','Coolpad','HTC','Panasonic','Huawei','LG']
num_list = [23, 35, 2, 12, 14, 5, 13, 14, 11, 14, 14, 9, 9, 11, 6,6,1,2,5,1,4]

# Loop through both lists
name = []
rating = []
rating_reviews_count = []
revised_price = []
original_price = []
discount = []
ram_rom_expandable = []
size = []
camera = []
battery = []
processor = []
reviews = []
description = []


# In[9]:


count = 0
for brand, count in zip(brands, num_list):
    for i in range(1, count + 1):
#         print(f"{brand} {i}")
        if i == 1:
            url = 'https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3D{}'.format(brand)
        else:
            url = 'https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3D{}&page={}'.format(brand,i)
        webpage = requests.get(url, headers = Header)
        soup = BeautifulSoup(webpage.content,'html.parser')
        mobile = soup.find_all('div', class_="tUxRFH")
#         count = count + len(mobile)
#         print(count)
        for k in mobile:
            name.append(k.find("div",class_ = 'KzDlHZ').text)
            
            
            count += 1
            print(count, "Name: ", k.find("div",class_ = 'KzDlHZ').text)
            
            if k.find("div",class_ = 'XQDdHH') == None:
                rating.append('None')
            else:
                rating.append(k.find("div",class_ = 'XQDdHH').text)
            
            
            if k.find("span",class_ = 'hG7V+4') == None:
                rating_reviews_count.append('')
            else:
                rating_reviews_count.append(k.find("span",class_ = 'hG7V+4').text)
            
            
            if k.find('div',class_ = 'Nx9bqj _4b5DiR') == None:
                revised_price.append('')
            else:
                revised_price.append(k.find('div',class_ = 'Nx9bqj _4b5DiR').text)
            
            
            if k.find('div',class_ = 'yRaY8j ZYYwLA') == None:
                original_price.append('')
            else:
                original_price.append(k.find('div',class_ = 'yRaY8j ZYYwLA').text)
            
            
            if k.find("div",class_ ='UkUFwK') == None:
                discount.append('')
            else:
                discount.append(k.find("div",class_ ='UkUFwK').text)
            
            
            if k.find_all('li')[0] == None:
                ram_rom_expandable.append('')
            else:
                ram_rom_expandable.append(k.find_all('li')[0])
            
            
            if k.find_all('li')[1] == None:
                size.append('')
            else:
                size.append(k.find_all('li')[1])
            
            
            if k.find_all('li')[2] == None:
                camera.append('')
            else:
                camera.append(k.find_all('li')[2])
            
            
            if len(k.find_all('li')) > 3:
                if k.find_all('li')[3] == None:
                    battery.append('')
                else:
                    battery.append(k.find_all('li')[3])
            else:
                battery.append('')
            
            
            if len(k.find_all('li')) > 4:
                if k.find_all('li')[4] == None:
                    processor.append('')
                else:
                    processor.append(k.find_all('li')[4])
            else:
                processor.append('')
                
                
            links = soup.find("a",attrs = {'class':"CGtC98",'target':'_blank','rel':'noopener noreferrer'})
            link = links.get('href')
            product_link = 'https://www.flipkart.com' + link
            new_webpage = requests.get(product_link, headers = Header)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")


# In[24]:


Mobile = pd.DataFrame({'Name':name[:4421], 'Rating': rating[:4421], 'rating_reviews_count': rating_reviews_count[:4421],'revised_price':revised_price[:4421],
             'original_price':original_price[:4421],'discount':discount[:4421],'ram_rom_expandable':ram_rom_expandable[:4421],'size':size[:4421],
             'camera':camera,'battery':battery[:4421],'processor':processor[:4421]},)


# In[25]:


Mobile


# In[29]:


Mobile.to_csv('C:/Users/DEV/Downloads/Mobile.csv',index=False)


# In[244]:


name_1 = []
reviews = []  # To store reviews
description = []  # To store descriptions

for brand, count in zip(brands, num_list):
    for i in range(1, count + 1):
        url = 'https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3D{}&page={}'.format(brand, i)
        webpage = requests.get(url, headers=Header)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        
        # Find mobile names
        mobiles = soup.find_all('div', class_="tUxRFH")
        count = 0
        for k in mobiles:
            mobile_name = k.find("div", class_='KzDlHZ').text
            name_1.append(mobile_name)
            count += 1
            print(f"Count: {count}, Mobile Name: {mobile_name}")
            
            # Get the link to the product (just one link per product)
            product_link_tag = k.find("a", attrs={'class': "CGtC98", 'target': '_blank', 'rel': 'noopener noreferrer'})
            if product_link_tag:
                product_link = 'https://www.flipkart.com' + product_link_tag.get('href')
                new_webpage = requests.get(product_link, headers=Header)
                new_soup = BeautifulSoup(new_webpage.content, "html.parser")
                
                # Get reviews (ensure you only fetch reviews once)
                reviews_1 = new_soup.find_all('div', class_="ZmyHeo")
                num_reviews = len(reviews_1)
                print(f"Number of reviews found for {mobile_name}: {num_reviews}")
                
                # Process up to 3 reviews or fewer if not available
                review_list = []
                for review_index in range(min(3, num_reviews)):
                    review_text = reviews_1[review_index].get_text(strip=True)
                    review_list.append(review_text)
                
                # If less than 3 reviews, append empty strings for missing ones
                while len(review_list) < 3:
                    review_list.append('')
                
                # Append the reviews to your list (make sure they are unique)
                reviews.append(review_list)

                # Get product description (if available)
                description_block = new_soup.find('div', class_="yN+eNk w9jEaj")
                description_text = description_block.get_text(strip=True) if description_block else ''
                description.append(description_text)
            else:
                print(f"No link found for mobile: {mobile_name}")

