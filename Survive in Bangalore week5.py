#!/usr/bin/env python
# coding: utf-8

# # My Capstone Project

# <hr>

# ## __Project Name__ :   
# # Survive in Bangalore

# <hr>

# ### In my project I am going to share you some idea about exploring new places using foursquare api.   
# ### Introduction/Business Problem:
# #### Suppose I have completed my Post Graduation in Statistics from Bhubaneswar, Odisha and moving to Bangalore for higher studies in Data science. Although you have much idea to survive in new places, asking to neighouberhood friends and your instructors also room-mate. But what if you havenot been to Bangalore prior to this, also you dont have bike to explore the new place. So dont worry about it, we have our friendly app foursquare to help us in our journey.    
# #### Using the Developer option we can gather data from all over the BTM Layout Area of Bangaluru, and use the relevent data for our decission making purpose.
# Right after Deciding Where to Study:   
# . Search for Nearby ATM to Collect cash.   
# . Search for Nearby PG.   
# . Search for Hotels, Cafe near your location.   
# 
# 

# <hr>

# ## Step: 1  
# ### Search for Nearby ATM and PG ?
# <hr>

# ### Lets Begin our project by Importing Required packages

# In[1]:


import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

#!conda install -c conda-forge geopy --yes 
#! pip install geopy
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

#!conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# In[2]:


CLIENT_ID = 'DIFB4NBGW2Q52A52H00ZYIODEVAQQAVE1KY5UWIABBS2VGDB' # your Foursquare ID
CLIENT_SECRET = 'MPI353I1EBJOZNL3ULJXFNA3EYJM5GQDRCGEAFJQ0KGNTKQV' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[3]:


address = '1st Stage, BTM Layout'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# #### latitude= 12.9171879 
# #### longitude=77.6088051

# #### The Place where we are going to stay is in "BTM Layout" so lets set our Location and set the radious of 2 km

# In[4]:


#search_query = 'Indian,solutions'
search_query = 'atm,pg'
radius = 2000
print(search_query + ' .... OK!')


# In[5]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[6]:


results = requests.get(url).json()
results


# In[7]:


# assign relevant part of JSON to venues
venues = results['response']['venues']

# tranform venues into a dataframe
dataframe = json_normalize(venues)
dataframe


# ### keep only columns that include venue name, and anything that is associated with location

# In[8]:


filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]


# In[9]:


dataframe_filtered.categories[0][0]['name']


# ### Filter the categories column

# In[10]:


def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# In[11]:


dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)


# In[12]:


dataframe_filtered[['location.lat','location.lng']].head()


# In[13]:


dataframe_filtered.categories.unique()


# #### Here we get our Data Frame to work with.

# In[14]:


dataframe_filtered.head(2)


# In[15]:


import folium


# #### Now Lets Plot the Map with required data Points

# In[16]:


def placecol(i):
    switch={
        'Bank':'blue',
        'Residential Building (Apartment / Condo)':'green',
        'Assisted Living':'green', 
        'ATM':'lightblue', 
        'Hostel':'orange', 
        None:'green', 
        'Housing Development':'lightgreen',
        'Building':'green',
    }
    return switch.get(i)


# In[17]:


df=dataframe_filtered


# In[18]:


df.head(2)


# ### ExcelR Solution 12.9172° N, 77.6142° E

# {'orange', 'beige', 'blue', 'white', 'lightgreen', 'darkblue', 'darkred', 'darkgreen', 'cadetblue', 'pink', 'purple', 'lightblue', 'lightgrayblack', 'lightred', 'green', 'gray', 'darkpurple', 'red'}

# In[19]:


Bangaluru = folium.Map(location=[latitude,longitude],zoom_start=15)
loc = folium.map.FeatureGroup()

for lt,ln,cat,nam in zip(df['location.lat'],df['location.lng'],df['categories'],df.name):
    loc.add_child(
        folium.CircleMarker(
            location=[lt,ln],
            color=placecol(cat),
            radious=5,
            fill=True,
            fill_color=placecol(cat),
            fill_opacity=0.6,
            popup=nam,
            
        )
    )
loc.add_child(
        folium.Marker(
            location=[12.9172,77.6142],
            popup='ExcelR Solutions',
            icon = folium.Icon(icon='book',color='darkblue')
          
        )
    )
Bangaluru.add_child(loc)


# #### Here is the Map Showing :   
# . Blue marks with ATM   
# . Green marks with PG
# . Yellow Marks are with 

# In[ ]:





# <hr>   
# 
# <hr>   

# ## Step 2:   
# ### Next Step is to See the Reviews of those PG, Where to Stay ?   
# 
# <hr>

# In[20]:


CLIENT_ID = 'DIFB4NBGW2Q52A52H00ZYIODEVAQQAVE1KY5UWIABBS2VGDB' # your Foursquare ID
CLIENT_SECRET = 'MPI353I1EBJOZNL3ULJXFNA3EYJM5GQDRCGEAFJQ0KGNTKQV' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[21]:


df_pgid=dataframe_filtered.loc[
                   dataframe_filtered.name.str.contains('PG') | 
                   dataframe_filtered.name.str.contains('pg') | 
                   dataframe_filtered.name.str.contains('Pg'),['name','id','location.lat','location.lng']]


# In[22]:


df_pgid.head()


# In[32]:


# For PG 1
venue_id = '5221dde4498e569a0b14fbd3' # ID of Harry's Italian Pizza Bar
url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)
url


# In[33]:


result = requests.get(url).json()
result
#result['response']['venue'].keys()


# In[ ]:





# In[25]:


df_pgid['Like'] = 0
df_pgid['contact'] = 'no number found'


# In[ ]:


for i,j,k in zip(df_pgid.id,df_pgid.name,df_pgid.index) :
    venue_id = i 
    url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)
    result = requests.get(url).json()
    A=result['response']['venue']['likes']['count']
    B=result['response']['venue']['contact'] 
    df_pgid.loc[k,'Like'] = A
    df_pgid.loc[k,'contact'] = str(B)
    print(A,j,B)
    


# #### Next Step is to See the Reviews of those PG, Where to Stay ?

# In[ ]:


df_pgid.loc[df_pgid['Like']==1]


# ### Lets Create our Map Again   
# #### Green marked pg are liked and yellow mark pg are never liked

# In[35]:


Bangaluru = folium.Map(location=[latitude,longitude],zoom_start=15)
loc = folium.map.FeatureGroup()
for lt,ln,name,like in zip(df_pgid['location.lat'],df_pgid['location.lng'],df_pgid['name'],df_pgid['Like']):
    if like==1:
        col='green'
        r=7
    else:
        col='yellow'
        r=5
    loc.add_child(
        folium.CircleMarker(
            location=[lt,ln],
            color=col,
            radious=r,
            fill=True,
            fill_color=col,
            fill_opacity=0.6,
            popup=name,
            
        )
    )
Bangaluru.add_child(loc)


# ### Conclusion   
# #### As Its India and less of us know about the Foursquare App, so due to less information, and no review in any PG. We conclude our step 2 with selecting those PG which are ever liked.

# <hr>
# <hr>

# ## Step 3:   
# ### Next Step is to See the Distance of those PG, From BTM Latout ?   
# 
# <hr>

# In[36]:


df_PG=dataframe_filtered.loc[
                   dataframe_filtered.name.str.contains('PG') | 
                   dataframe_filtered.name.str.contains('pg') | 
                   dataframe_filtered.name.str.contains('Pg')]


# In[37]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[43]:


df_PG = df_PG.set_index('name')


# In[45]:


df_PG[['location.distance']].head(2)


# In[46]:


df_PG[['location.distance']].plot(kind='barh',figsize=(8,6),color='gold')


# ## Conclusion

# #### Ok now having a mare look in oud data and the plot , we conclude that , we gonna live in Shri Sai Bhabani PG

# ## After more research This Project will continue.........................
