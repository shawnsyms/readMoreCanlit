#!/usr/bin/env python
# coding: utf-8

# # #readMoreCanlit | Notebook 2: Data cleaning and visualization

# <center><img src='../img/readMoreCanlit.png'></center>

# <a name="contents"></a>
# ## Contents
# 
# * <a href="#overview">Overview</a><br>
# * <a href="#imports">Imports</a><br>
# * <a href="#data-manipulation">Data manipulation</a><br>
# * <a href="#visualization">Visualization</a><br>

# <a name="overview"></a>
# ## Overview

# This section of the notebook involves manipulating the text in ways that help with how I want the application to display it. The Canadian and international dataframes are concatenated rows-size into one, and several new features are added: (1) the author and title information is concatenated column-wise into a single feature, and title, author and description information are likewise concatenated into a single details feature that contains all information regarding each book. Columns containing the word count and character count for each details section are added, and some visualization has been implemented to help bring the data to life.

# <a name="imports"></a>
# ## Imports

# In[58]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter
from wordcloud import STOPWORDS, WordCloud

# This magic line will allow you to generate plots within the Jupyter notebook
get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.display.max_seq_items = 2000
pd.options.display.max_rows = 4000


# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# <a name="data-manipulation"></a>
# ## Data manipulation

# Let's concatenate a few columns to set up the data the way our presentation layer will eventually want it displayed. And let's calculate a few numerical columns that we can use for visualization purposes.

# In[59]:


# # Write a function to carry out the desired data manipulation
# NOTE: I'm still troubleshooting this function
# def data_manipulation(df):
#     print('../data/processed/' + df + '_pre.csv')
#     df = pd.read_csv('../data/processed/' + df + '_pre.csv', encoding = "ISO-8859-1")
#     df = df.applymap(str)
#     df.dropna(axis = 0, how ='any', inplace = True)
#     df['book'] = df['title'] + ' by ' + df['author']
#     df['details'] = df['book'] + ': ' + df['description']
#     df.drop(['title', 'author', 'description'], axis=1, inplace=True)
#     df['character_count'] = df['details'].astype(str).apply(len)
#     df['word_count'] = df['details'].apply(lambda x: len(str(x).split()))
#     df.to_csv('../data/processed/' + df + '_post.csv')


# In[60]:


data_manipulation(canadian)
data_manipulation(international)


# In[61]:


# Original data manipulation code pre-function

# First the Canadian dataset
canadian = pd.read_csv('../data/processed/canadian_pre.csv', encoding = "ISO-8859-1")
canadian = canadian.applymap(str)
canadian.dropna(axis = 0, how ='any', inplace = True)
canadian['book'] = canadian['title'] + ' by ' + canadian['author']
canadian['details'] = canadian['book'] + ': ' + canadian['description']
canadian.drop(['title', 'author', 'description'], axis=1, inplace=True)
canadian['character_count'] = canadian['details'].astype(str).apply(len)
canadian['word_count'] = canadian['details'].apply(lambda x: len(str(x).split()))
canadian.to_csv('../data/processed/canadian_post.csv')

# And then the international one
international = pd.read_csv('../data/processed/international_pre.csv', encoding = "ISO-8859-1")
international = international.applymap(str)
international.dropna(axis = 0, how ='any', inplace = True)
international['book'] = international['title'] + ' by ' + international['author']
international['details'] = international['book'] + ': ' + international['description']
international.drop(['title', 'author', 'description'], axis=1, inplace=True)
international['character_count'] = international['details'].astype(str).apply(len)
international['word_count'] = international['details'].apply(lambda x: len(str(x).split()))
international.to_csv('../data/processed/international_post.csv')


# In[62]:


# Let's have a look
canadian


# In[63]:


# Concatenate the two dataframes rows-wise so we have one source for our corpus

books = pd.concat([canadian, international])


# In[64]:


books.tail()


# In[65]:


# Reset the index to avoid conflicts between the indices of the two former dataframes

books.reset_index(drop=True)


# In[66]:


# Save a copy back to disk

books.to_csv('../data/processed/books.csv')


# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# <a name="visualization"></a>
# ## Visualization

# #### Word clouds

# In[45]:


literary_stopwords = ['amazon best book of the year', 'arthur ellis', 'astonishing', 'author', 'award', 'award-winning', 'best', 'best book of the year', 'bestseller', 'bestselling', 'book', 'book award', 'boston globe', 'canada reads', 'category', 'character', 'classic', 'critically acclaimed', 'debut', 'entertainment weekly', 'epic', 'finalist', 'finalist', 'foremost', 'giller prize', 'giller prize', 'globe and mail', 'governor generals award', 'governor generals literary award', 'harpercollins', 'heralded', 'highly anticipated', 'kobo', 'literary', 'literature', 'longlisted', 'national bestseller', 'nationally', 'new york times', 'novel', 'prize', 'prize-winning', 'publish', 'publishers weekly', 'rogers writers trust', 'scotiabank', 'shortlisted', 'story', 'ubc', 'widely anticipated', 'winner', 'writers trust fiction prize', 'writers trust of canada']
stoplist = set(stopwords.words('english') + list(punctuation) + literary_stopwords)
path = '../data/processed/canadian_post.csv'
df = pd.read_csv(path)
df = df.applymap(str)
texts = df['details'].str.lower()
word_counts = Counter(word_tokenize('\n'.join(texts)))
words_list = word_counts.most_common()
words_list


# <img src='../img/canadian_word_cloud.png'>

# In[49]:


canadian_words = pd.read_csv('../data/processed/canadian_words.csv')


# In[50]:


canadian_words


# In[57]:


sns.set(style="darkgrid")
ax = sns.countplot(x="word", data=canadian_words)


# <div style="text-align: right">(<a href="#contents">home</a>) </div>

# In[39]:


books['origin'].hist()


# In[40]:


books['word_count'].hist()


# These visualizations are obviously not that good and this section is a work in progress! In the next section, I implement the recommender system.

# <div style="text-align: right">(<a href="#contents">home</a>) </div>
