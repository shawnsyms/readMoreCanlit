#!/usr/bin/env python
# coding: utf-8

# # #readMoreCanlit | Notebook 3: Recommender system

# <center><img src='../img/readMoreCanlit.png'></center>

# <a name="contents"></a>
# ## Contents
# 
# * <a href="#overview">Overview</a><br>
# * <a href="#imports">Imports</a><br>
# * <a href="#preprocessing">Data sources</a><br>
# * <a href="#modeling">Modeling</a><br>
# > * <a href="#tfidf">TFIDF Vectorizer</a><br>
# > * <a href="#recommender">Recommender</a><br>
# > * <a href="#recommend-books-by-bookid">Recommend books by bookID</a><br>
# > * <a href="#recommend-books-by-title">Recommend books by title</a><br>

# <a name="overview"></a>
# ## Overview

# <img src='../img/diagram.jpg'>

# <a name="imports"></a>
# ### Imports

# In[94]:


# pandas and numpy
import pandas as pd
import numpy as np

# nltk imports
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

# sci-kit learn imports
from sklearn.compose import make_column_transformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
from sklearn.pipeline import Pipeline, make_pipeline

# Presentation and visuals
import seaborn as sns
import matplotlib.pyplot as plt

# This magic line will allow you to generate plots
# within the Jupyter notebook.
get_ipython().run_line_magic('matplotlib', 'inline')
from pprint import pprint
pd.options.display.max_seq_items = 2000
pd.options.display.max_rows = 4000
# pd.set_option(display.max_columns), None

# other imports
import json
import lxml
from lxml import html
import random
import regex as re
import requests
import time
import urllib.request
from datetime import datetime

import warnings
warnings.filterwarnings(action='once')


# In[95]:


# Read in the data

df = pd.read_csv('../data/processed/canadian_post.csv', encoding = "ISO-8859-1")

try:
    df.drop(columns=['Unnamed: 0'], inplace = True)
    
except: 
    pass


# In[96]:


# Confirm there are no nulls

df.isnull().sum()


# In[97]:


# Look up a sample entry

df.loc[df['id'] == 6890]


# <a name="preprocessing"></a>
# ### Preprocessing
# 

# In[98]:


# NOTE: I still need to integrate this into preprocessing

# Create a stopwords list of meta-critical commentary vocabulary 
#to be removed from the Canadian dataset as part of preprocessing

literary_stopwords = ['amazon best book of the year', 'arthur ellis', 'astonishing', 'author', 'award', 'award-winning', 'best', 'best book of the year', 'bestseller', 'bestselling', 'book', 'book award', 'boston globe', 'canada reads', 'category', 'character', 'classic', 'critically acclaimed', 'debut', 'entertainment weekly', 'epic', 'finalist', 'finalist', 'foremost', 'giller prize', 'giller prize', 'globe and mail', 'governor generals award', 'governor generals literary award', 'harpercollins', 'heralded', 'highly anticipated', 'kobo', 'literary', 'literature', 'longlisted', 'national bestseller', 'nationally', 'new york times', 'novel', 'prize', 'prize-winning', 'publish', 'publishers weekly', 'rogers writers trust', 'scotiabank', 'shortlisted', 'story', 'ubc', 'widely anticipated', 'winner', 'writers trust fiction prize', 'writers trust of canada']


# In[99]:


# Preprocess the posting content; this should take under 2 minutes
# start an empty list to hold preprocessed postings

# Create a column to capture the preprocessed book descriptions
# separate from the originals

df['details_preprocessed'] = np.nan

# Now preprocess the text

for i in range(len(df)):  # for each full_entry
    details = re.sub('[^a-zA-Z]', ' ', df['details'][i]) # remove non text characters
    details = details.lower() # lower-case everything
    details = details.split() # split into words
#     ps = PorterStemmer() # instantiate the Porter word stemmer
#     details = [ps.stem(word) for word in details if not word in set(stopwords.words('english'))] # reduce to only stemmed non-stopwords    desc = ' '.join(desc) # reassemble the string
    df['details_preprocessed'][i] = details # write the preprocessed text back to the df


# In[100]:


df['book']


# In[102]:


# Have a look

df['book'][6781]


# <a name="modeling"></a>
# ## Modeling

# <a name="tfidf"></a>
# ### TF-IDF

# In[103]:


# Instantiate a TFIDF vectorizer, fit it to the data, transform the data
# in the df['details'] column, and implement cosine similarity via Linear Kernel

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['details'])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)


# In[104]:


tfidf_matrix


# In[64]:


# Have a look at cosign similarities

cosine_similarities[0]


# <a name="recommender"></a>
# ### Recommender

# In[88]:


# Create a dictionary that maps cosine similarities back to rows in the dataframe

results = {}

for idx, row in df.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], df['id'][i]) for i in similar_indices]
    results[row['id']] = similar_items[1:]


# In[89]:


# Have a look

results


# <a name="recommend-books-by-bookid"></a>
# ### Recommend books by bookID

# In[90]:


# Function for book lookup

def book(id):
    return df.loc[df['id'] == id]['book'].tolist()[0].split(' - ')[0]


# In[91]:


def book_recommendation_by_id(id, num):
    print("Here are " + str(num) + " books that are similar to " + book(id) + ":")
    print("-------")
    print("Read more Canlit!")
    recommendations = results[id][:num]
    for recommendation in recommendations:
        print("For you, I recommend " + book(recommendation[1]) + " (whose similarity score is:" + str(recommendation[0]) + ")")


# In[92]:


# Look up a book by title

df.loc[df['book'] == 'Nothing Looks Familiar by Shawn Syms']['id'].to_list()


# In[93]:


# Call the functions to make a recommendation

try:
    book_recommendation(id=6889, num=5)
    
except: 
    print("I'm sorry, I don't know about that book")


# <a name="recommend-books-by-title"></a>
# ### Recommend books by title

# In[ ]:


def book_title(title):
    return df.loc[df['book'] == id]['book'].tolist()[0].split(' - ')[0]    


# In[ ]:


def book_recommendation_by_title(id, num):
    print("Here are " + str(num) + " books that are similar to " + book(id) + ":")
    print("-------")
    print("Read more Canlit!")
    recommendations = results[id][:num]
    for recommendation in recommendations:
        print("For you, I recommend " + book(recommendation[1]) + " (whose similarity score is:" + str(recommendation[0]) + ")")


# In[83]:


my_fave_book = input("Tell me about your favourite book, and I'll recommend some great Canadian reads!")


# <div style="text-align: right">(<a href="#contents">home</a>) </div>
