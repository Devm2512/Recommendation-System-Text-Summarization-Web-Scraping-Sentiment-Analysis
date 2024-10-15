#!/usr/bin/env python
# coding: utf-8

# In[426]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[427]:


df = pd.read_csv('C:/Users/DEV/Downloads/Mobile.csv')


# In[428]:


df


# In[429]:


df['processor'][0]


# In[430]:


df.info()


# # Redundancies in the Dataset

# **1. Rating Column**
# It should be Float value. it is of string value
# 
# **2. Rating and Reviews Count**
# There is no information in this column. DROP IT.
# 
# **3. Revised Price**
# It should be an integer value. It is given as a string
# 
# **4. original_price**
# It should be an integer value. It is given as a string
# 
# **5. Discount**
# It should be an integer value. It is given as a string. also, rename the column to 'discount in %'.
# 
# **6. ram_rom_expandable**
# Create new column from existing ones. Ram and ROM.These columns should be integers. Also, There is a HTML tag, remove it.
# 
# **7. Size**
# Create a new column. name it 'size in inches'. The column should be a float.
# 
# **8. Camera**
# Create 2 new columns. Front camera and backcamera. The datatype should be float. Remove HTML tags
# 
# **9. Battery**
# Change the column name to battery in MaH. Also, the Datatype should be Inteter.
# 
# **10. Processor**
# Remove the word process.

# # Strategy

# We first perform create new columns from the data. The convert the datatypes. In the end we change the name of columns wherever required. Finally we remove the redundant columns.

# # Removing HTML Tags

# ### ram_rom_expandable

# In[431]:


# Remove HTML tags
df['ram_rom_expandable'] = df['ram_rom_expandable'].str.replace(r'<.*?>', '', regex=True)


# ### Size

# In[432]:


df['size'] = df['size'].str.replace(r'<.*?>', '', regex=True)


# ### Camera

# In[433]:


df['camera'] = df['camera'].str.replace(r'<.*?>', '', regex=True)


# ### Battery

# In[434]:


df['battery'] = df['battery'].str.replace(r'<.*?>', '', regex=True)


# ### Processor

# In[435]:


df['processor'] = df['processor'].str.replace(r'<.*?>', '', regex=True)


# # Creating New Columns

# ### ram_rom_expandable

# In[436]:


df['ram'] = df['ram_rom_expandable'].str.split('|').str.get(0)


# In[437]:


df['rom'] = df['ram_rom_expandable'].str.split('|').str.get(1)


# In[438]:


df['expandable'] = df['ram_rom_expandable'].str.split('|').str.get(2)


# ### Camera

# In[439]:


df['camera'] = df['camera'].str.split('|').str.get(0)


# In[440]:


df['front_camera'] = df['camera'].str.split('|').str.get(1)


# In[441]:


df


# ### Extracting size in inches 

# In[442]:


df['size'] = df['size'].str.split(' ').str.get(2).str.split('(').str.get(1)


# ### Battery

# In[443]:


df['battery'].unique()

In the above, we can see the unique values in the battery column. There ae 3 types of data in there
1. Battery info in MaH
2. Processor info (This info is regarding all the apple iphones) 
3. Display size ( It is the information of the phones that are refurbished)

So we first drop all the refurbshied phones.
Then in the second step we filter the data for iphone, then we transfer the processor info from battery column to processor column. To do that we first need to filter the data only for iphones. so we create a new feature, 'BRAND' 
as for the null values in battery column we try to find out what is the value of MaH for ihpone batteries
# In[444]:


df[df['battery'] == '6.1 inch Display']


# In[445]:


df = df[df['ram_rom_expandable']!='Grade: Refurbished - Superb']


# In[446]:


df = df[df['battery'] != '6.5 inch HD+ Display']


# In[447]:


df['battery'].unique()


# In[448]:


df['brand'] = df['Name'].str.split(' ').str.get(0)


# In[449]:


df['brand'].unique()


# In the aboe code, the unqiue value of brand can be seen. now, here we have same brand but are considered different
# 1. SAMSUNG - Samsung
# 2. MOTOROLA - Motorola
# we need to change it.

# In[450]:


brand_name = {"Samsung":'SAMSUNG','Motorola':"MOTOROLA"}


# In[451]:


df['brand'] = df['brand'].replace(brand_name)


# In[452]:


df['brand'].unique()


# Now we filter the apple data

# In[453]:


apple = (df['brand']=='Apple')


# In[454]:


df[apple]


# In[455]:


# Code for moving processor frombattery to processor column
df.loc[apple, 'processor'] = df.loc[apple, 'battery']


# In[456]:


df.loc[apple, 'battery'] = '3600 mAh Battery'


# In[457]:


df


# Now, if you look closely, you can see again for apple iphone the ROM value are in RAM column. so we have created a mask earlier we use that only to move the rom value from ram column

# In[458]:


df.loc[apple,'rom'] = df.loc[apple,'ram']


# In[459]:


df['name'] = df['Name'].str.split('(').str.get(0)


# In[460]:


# now we change the ram value as well
df


# In[461]:


df['name']= df['name'].str.strip()


# In[462]:


iphone_ram_data = {
    "Apple iPhone 15": "8 GB (LPDDR5)",
    "Apple iPhone 15 Plus": "8 GB (LPDDR5)",
    "Apple iPhone 15 Pro": "8 GB (LPDDR5)",
    "Apple iPhone 15 Pro Max": "8 GB (LPDDR5)",
    "Apple iPhone 16": "8 GB (LPDDR5)",
    "Apple iPhone 12": "8 GB (LPDDR5)",
    "Apple iPhone 16 Plus": "8 GB (LPDDR5)",
    "Apple iPhone 13": "8 GB (LPDDR5)",
    "Apple iPhone 14 Plus": "8 GB (LPDDR5)",
    "Apple iPhone 16 Pro": "8 GB (LPDDR5)",
    "Apple iPhone 16 Pro Max": "8 GB (LPDDR5)",
    "Apple iPhone 14": "8 GB (LPDDR5)",
    "Apple iPhone 11": "8 GB (LPDDR5)",
    "Apple iPhone XR": "8 GB (LPDDR5)",
    "Apple iPhone 8": "8 GB (LPDDR5)",
    "Apple iPhone XS Max": "8 GB (LPDDR5)",
    "Apple iPhone SE 3rd Gen": "8 GB (LPDDR5)",
    "Apple iPhone 14 Pro": "8 GB (LPDDR5)",
    "Apple iPhone XS": "8 GB (LPDDR5)",
    "Apple IPhone 4": "8 GB (LPDDR5)",
    "Apple iPhone 7": "8 GB (LPDDR5)",
    "Apple iPhone 7 Plus": "8 GB (LPDDR5)",
    "Apple iPhone 12 mini": "8 GB (LPDDR5)",
    "Apple iPhone SE": "8 GB (LPDDR5)",
    "Apple iPhone 14 Pro Max": "8 GB (LPDDR5)",
    "Apple iPhone 11 Pro": "8 GB (LPDDR5)",
    "Apple iPhone 12 Pro Max": "8 GB (LPDDR5)",
    "Apple iPhone 13 Pro Max": "8 GB (LPDDR5)",
    "Apple iPhone X": "8 GB (LPDDR5)",
    "Apple iPhone 11 Pro Max": "8 GB (LPDDR5)",
    "Apple iPhone 6 Plus": "8 GB (LPDDR5)",
    "Apple iPhone 13 Pro": "8 GB (LPDDR5)",
    "Apple iPhone 12 Pro": "8 GB (LPDDR5)",
    "Apple iPhone 6s Plus": "8 GB (LPDDR5)",
    "Apple iPhone 13 mini": "8 GB (LPDDR5)",
    "Apple iPhone 8 Plus": "8 GB (LPDDR5)",
    "Apple iPhone 6s": "8 GB (LPDDR5)",
    "Apple iPhone 5s": "8 GB (LPDDR5)",
    "Apple iPhone 6": "8 GB (LPDDR5)",
    "Apple iPhone 5C": "8 GB (LPDDR5)"
}


# In[463]:


def update_ram(row):
    model = row['name']
    return iphone_ram_data.get(model, row['ram'])


# In[464]:


df['ram'] = df.apply(update_ram, axis=1)


# In[465]:


df


# In[466]:


df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)


# In[467]:


# now we change the datatypes of the columns


# In[468]:


df['revised_price'] = df['revised_price'].str.replace(',','').str.replace('₹','')


# In[469]:


df['original_price'] = df['original_price'].str.replace(',','').str.replace('₹','')


# In[470]:


df['discount'] = df['discount'].str.split('%').str.get(0)


# In[471]:


df['battery'] = df['battery'].str.split(' ').str.get(0)


# In[472]:


df['ram'] = df['ram'].str.split(' ').str.get(0)


# In[473]:


df['rom'] = df['rom'].str.strip().str.split(' ').str.get(0)


# In[474]:


df['expandable'] = df['expandable'].str.strip().str.split(' ').str.get(2)


# In[477]:


df['front_camera'] = df['camera'].str.split('+').str.get(0).str.replace('MP','').str.split(' ').str.get(0).str.replace('Mp','').str.replace('Rear','24').astype('float') + df['camera'].str.split('+').str.get(1).str.replace('MP','').str.strip().str.split(' ').str.get(0).str.replace('AI','48').str.replace('Depth','24').str.replace('Low','25').fillna(24).astype('float')


# In[478]:


df = df.drop(columns = ['original_price','discount','expandable','rating_reviews_count','ram_rom_expandable','Name','camera'],axis =1)


# In[479]:


df = df.dropna()


# In[480]:


df


# In[481]:


df['ram'] = df['ram'].str.replace('56','6')


# In[482]:


df['ram'] = df['ram'].str.replace('512','0.5')


# In[483]:


df['rom'] = df['rom'].str.replace('Expandable','16')


# In[484]:


def changing_dtype(dataframe, column, dtype):
    dataframe[column] = dataframe[column].astype(dtype)


# In[485]:


changing_dtype(df,'revised_price','int32')


# In[486]:


changing_dtype(df,'size','float')


# In[487]:


changing_dtype(df,'battery','int32')


# In[488]:


changing_dtype(df,'ram','float')


# In[489]:


changing_dtype(df,'rom','float')


# In[490]:


changing_dtype(df,'front_camera','float')


# In[491]:


changing_dtype(df,'Rating','float')


# In[492]:


df = df.drop_duplicates(subset = ['name'])


# In[493]:


df


# In[496]:


df.to_csv('C:/Users/DEV/Downloads/Mobile_data_cleaned.csv')


# In[ ]:




