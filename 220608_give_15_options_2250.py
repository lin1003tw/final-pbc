#!/usr/bin/env python
# coding: utf-8

# In[68]:


import googlemaps
import pandas as pd
import time
google_key = 'AIzaSyB74lRYR0Y-8FGxnFAoW0V8Wv6GEcKmbr8' # fill in your google map api key
gmaps = googlemaps.Client(key=google_key)


# In[75]:


from io import BytesIO
from PIL import Image
def time_transform(row):
    if pd.isna(row):
        return {}
    return row['weekday_text']

def image_transform(row):
    # print(row)
    b = row[0]['photo_reference']
    f = BytesIO()
    for chunk in gmaps.places_photo(photo_reference = b, max_width=800, max_height=800):
        if chunk:
            f.write(chunk)
    image = Image.open(f)
    return image


# In[84]:


def find_sex_place(query: str, place_type: str):
    if place_type != 'hotel':
        ids = []
        results = []
        # Geocoding an address
        geocode_result = gmaps.geocode(query)
        loc = geocode_result[0]['geometry']['location']
        query_result = gmaps.places_nearby(type='bar',location=loc, radius=1000)
        results.extend(query_result['results'])
        while query_result.get('next_page_token'):
            time.sleep(2)
            query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
            results.extend(query_result['results'])
        print(f'Number of bars in {query}: {len(results)} (maximum: 60)')
        for place in results:
            ids.append(place['place_id'])
        stores_info = []
        for id in ids:
            stores_info.append(gmaps.place(place_id=id, language='zh-TW')['result'])
        print(f'Total number of bars: {len(stores_info)}')
        taipei_bar = pd.DataFrame.from_dict(stores_info)
        taipei_bar['score'] = taipei_bar['rating'] * taipei_bar['user_ratings_total']
        bar_df = taipei_bar.sort_values('score', ascending=False).head(15)
        bar_df['營業時間'] = bar_df['opening_hours'].apply(time_transform)
        bar_df['圖片'] = bar_df['photos'].apply(image_transform)
        if place_type == 'bar':
            return bar_df
    
    if place_type != 'bar':
        ids = []
        results = []
        geocode_result = gmaps.geocode(query)
        loc = geocode_result[0]['geometry']['location']
        query_result = gmaps.places_nearby(type='lodging',location=loc, radius=1000)
        results.extend(query_result['results'])
        while query_result.get('next_page_token'):
            time.sleep(2)
            query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
            results.extend(query_result['results'])
        print(f'Number of hotels in {query}: {len(results)} (maximum: 60)')
        for place in results:
            ids.append(place['place_id'])
        stores_info = []
        for id in ids:
            stores_info.append(gmaps.place(place_id=id, language='zh-TW')['result'])
        print(f'Total number of hotels: {len(stores_info)}')
        taipei_hotel = pd.DataFrame.from_dict(stores_info)
        taipei_hotel['score'] = taipei_hotel['rating'] * taipei_hotel['user_ratings_total']
        hotel_df = taipei_hotel.sort_values('score', ascending=False).head(15)
        hotel_df['營業時間'] = hotel_df['opening_hours'].apply(time_transform)
        hotel_df['圖片'] = hotel_df['photos'].apply(image_transform)
        if place_type == 'hotel':
            return hotel_df
        
    return pd.concat([bar_df, hotel_df])


# In[85]:


a = find_sex_place(query='南京復興站', place_type='hotel')
a


# In[86]:





# In[ ]:




