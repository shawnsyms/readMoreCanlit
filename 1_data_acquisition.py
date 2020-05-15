#!/usr/bin/env python
# coding: utf-8

# # #readMoreCanlit | Notebook 1: Data acquisition

# <center><img src='../img/readMoreCanlit.png'></center>

# <a name="contents"></a>
# ## Contents
# 
# * <a href="#overview">Overview</a><br>
# * <a href="#imports">Imports</a><br>
# * <a href="#data-sources">Data sources</a><br>
# * <a href="#get-international-book-metadata">Get international book metadata</a><br>
# * <a href="#get-canadian-book-metadata">Get Canadian book metadata</a><br>
# * <a href="#get-canadian-book-cover-art">Get Canadian book cover art</a><br>

# <a name="overview"></a>
# ## Overview

# To populate the corpus and app, three sets of data needed to be gathered:
# 
# > 1. information on international books (title, author, description)
# > 2. information on Canadian books (title, author, description)
# > 3. book cover art for Canadian books
# 
# For the international books, a broad search was undertaken to find lists of ISBNs (the international standard book number used in publishing to distinguish books/editions from one another) online. Sources were found at openlibrary.org and data.world that included over 2.7 million ISBNs (the lists contain the ISBN and no further information). 
# 
# To gather the necessary metadata, the ISBNdb.com API was employed to query a database of 12 million books. Progress was slow, however. First, there was a limitation of 15,000 queries per day. Second, the ISBNdb.com database is incomplete; many ISBNs had no entry in the database and of those that were present, many of them lacked descriptions (the primary piece of metadata that is required for the recommender system to work effectively. On average, about 5 percent of the returned ISBN information was usable. Over 100,000 ISBN queries were executed to produce a dataset of 6,000 international titles.
# 
# Canadian titles were more easily sourced via the website 49thshelf.com. Through webscraping, a set of URLs was requested in order to produce a set of title, author and description information for 8,500 Canadian fiction titles (it was not possible to differentiate the international titles by genre). The website provided book cover images for all of the titles as well.
# 

# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# <a name="imports"></a>
# ## Imports

# In[2]:


# pandas and numpy
import pandas as pd
import numpy as np

# other imports
from bs4 import BeautifulSoup
import json
import requests
import time
import urllib.request
from datetime import datetime

pd.options.display.max_seq_items = 2000
pd.options.display.max_rows = 4000


# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# <a name="get-international-book-metadata"></a>
# ## Get international book metadata

# In this section of the notebook, I use the ISBNdb.com API to query their database with a long list of ISBNs. The code in this section was rerun many times over a period of days. To run this code, you will need to uncomment it, acquire your own API code and membership to ISBNdb.com. The assembled data is in the repo in the /data folder.

# In[27]:


# Read in the ISBN list

isbn = pd.read_csv('../data/data_acquisition/international_for_download.csv')

# My for loop below requires the ISBNs to be interpreted as strings so they can be interpolated into URLs
isbn = isbn.applymap(str)

# Confirm the change
isbn.dtypes


# In[28]:


# Reduce to a subset matching the ISBNdb.com daily limit

isbn = isbn[0:15000]
isbn


# In[29]:


# Iterate through dataframe containing the list of ISBNs, 
# constructing URLs to pass to requests
# along with the ISBNdb authorization key
# return the necessary content in JSON format
# and write it back into the dataframe

# Note, this process was repeated many times
# it is commented out so I don't incur costs if all cells are run

# for j in range(len(isbn)):

#     header = {'Authorization': 'YOUR API KEY HERE'}
#     base_url = ('https://api2.isbndb.com/book/')
#     response = requests.get(base_url + isbn['isbn'][j], headers=header)
#     payload = response.json()
      
#     try:
#         isbn['title'][j] = payload['book']['title']
    
#     except:
#         isbn['title'][j] = np.nan
    
#     try:
#         isbn['authors'][j] = payload['book']['authors']
    
#     except:
#         isbn['authors'][j] = np.nan
              
#     try:
#         isbn['overview'][j] = payload['book']['overview']
    
#     except:
#         isbn['overview'][j] = np.nan
  
#     print('Info downloaded for book ' + str(j + 1) + ' of ' +  str(len(isbn)) + ' books.')
              
#     time.sleep(1)
    


# In[30]:


# Drop the ISBN column now that it is no longer needed
# and save the current set of international book metadata out to csv
# with the file named for the current date and time.

now = datetime.now()
dt = now.strftime("%d-%m-%Y_%H-%M-%S")


isbn.drop('isbn', axis=1, inplace=True)
isbn.to_csv('../data/saved/isbn' + dt +'.csv', index = False)

# Note that this process was repeated many times to assemble the 
# international portion of the app's dataframe


# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# <a name="get-canadian-book-metadata"></a>
# ## Get Canadian book metadata

# In this section of the notebook, I connect to the website 49thshelf.com in order to access descriptions of Canadian books used by the model. Uncomment the relevant code to run the download process. This code only needs to be run once, but it will take about 24 hours to complete. The data is in the repo in the /data folder.

# In[ ]:


# Read in the list of Canadian ISBNs
canadian = pd.read_csv('../data/data_acquisition/canadian_for_download.csv')

# My for loop below requires the ISBNs to be interpreted as strings so they can be interpolated into URLs

canadian = canadian.applymap(str)

# Confirm the change
canadian 


# In[ ]:


# Start an empty list to house the descriptions
# Iterate through the Canadian book metadata dataframe (populated from a csv);
# Grab the URL where the book description lives and use beautifulsoup
# to grab the relevant content; at the end, write it all back to the dataframe

# description_list = []

# for c in (range(len(canadian))):
#     response = requests.get(canadian['title_url'][c])
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     try:
#         for tag in soup.find_all("meta"):
#             if tag.get("property", None) == "og:description":
#                 print(tag.get("content", None))
#                 description = tag.get("content", None)
#                 description_list.append(description)
#     except:
#         description_list.append(np.nan)
        
        
#     time.sleep(2)
        
# canadian['description'] = description_list


# In[ ]:


# Drop the ISBN column now that it is no longer needed
# and save the current set of Canadian book metadata out to csv
# with the file named for the current date and time.

canadian.drop('isbn', axis=1, inplace=True)
canadian.to_csv('../data/processed/canadian_books.csv', index = False)
canadian.shape

# Note: This process was run once to populate the Canadian book metadata dataframe


# In[6]:


canadian = pd.read_csv('../data/processed/canadian_pre.csv')

# Remove duplicate entries from the dataframe
canadian = canadian.drop_duplicates(subset='title', keep="first")
canadian.to_csv('../data/processed/canadian_pre.csv', index = False)


# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# <a name="get-canadian-book-cover-art"></a>
# ## Get Canadian book cover art

# In this section, I use the data assembled in the previous section, which included URLs for cover images of the books. Running this process would involve uncommenting the code, and waiting for the downloads, which take about 24 hours, to complete. 

# In[8]:


# Read in the list of Canadian book metadata
# that contains URLs for book-cover imagery
images = pd.read_csv('../data/processed/canadian_books.csv')

# My for loop below requires the ISBNs to be interpreted as strings so they can be interpolated into URLs
images = images.applymap(str)

# Confirm the change
images.dtypes


# In[9]:


# for i in range(len(images)):

#     try:
#         urllib.request.urlretrieve(images['image'][i], '../img/books/' + images['id'][i] + '.jpg')
#         print('Just captured image number ' + images['id'][i])

#     except:
#         print('Failed to capture image number ' + images['id'][i])
        
#     time.sleep(2)


# In[ ]:


# Drop the column with the image URLs as it's no longer needed
images.drop(columns='image', inplace=True)

# And resave to the file
images.to_csv('../data/processed/canadian_books.csv', index = False)


# Through running the processes in this notebook as many times as needed, I was about to build a database of 6,500+ Canadian titles and 10,000+ international titles. Next, they will go through some feature engineering and preprocessing to become ready to be run through the TFIDF Vectorizer (which will change the words into numerical values that a model can understand and compare with one another. 

# <div style="text-align: right">(<a href="#contents">home</a>) </div>
