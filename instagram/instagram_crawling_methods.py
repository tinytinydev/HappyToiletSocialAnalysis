from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import os
import requests
import datetime as dt

def get_date(created):
    return dt.datetime.fromtimestamp(int(created))


# In[28]:

def get_csv_from_username(username):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)

    browser.get('https://www.instagram.com/'+username+'/?hl=en')

    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    links = []
    source = browser.page_source

    data = bs(source, 'html.parser')

    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
         if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com' + link.get('href'))
    
    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")
    links = []
    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
         if re.match("/p", link.get('href')):
             links.append('https://www.instagram.com' + link.get('href'))

    #sleep time is required. If you don't use this Instagram may interrupt the script and doesn't scroll through pages

    time.sleep(5) 
    Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/3.0);")
    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
         if re.match("/p", link.get('href')):
             links.append('https://www.instagram.com' + link.get('href'))
            

    result = pd.DataFrame()
    #for i in range(len(links)):
    for link in links:
        try:
            page = urlopen(link).read()
            data = bs(page, 'html.parser')
            body = data.find('body')
            script = body.find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')

            json_data = json.loads(raw)

            posts = json_data['entry_data']['PostPage'][0]['graphql']
            posts = json.dumps(posts)
            posts = json.loads(posts)

            x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
            x.columns = x.columns.str.replace("shortcode_media.", "")
            result = result.append(x)
        except:
            np.nan

    # Just check for the duplicates
    result = result.drop_duplicates(subset = 'shortcode')
    result.index = range(len(result.index))
    
    result.to_csv(path_or_buf="./docs/username_post.csv")

def get_csv_from_hashtag(hashtag):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)

    browser.get('https://www.instagram.com/explore/tags/'+ hashtag)

    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    links = []
    source = browser.page_source

    data = bs(source, 'html.parser')

    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
         if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com' + link.get('href'))
    
    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")
    links = []
    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
         if re.match("/p", link.get('href')):
             links.append('https://www.instagram.com' + link.get('href'))

    #sleep time is required. If you don't use this Instagram may interrupt the script and doesn't scroll through pages

    time.sleep(5) 
    Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/3.0);")
    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
         if re.match("/p", link.get('href')):
             links.append('https://www.instagram.com' + link.get('href'))
            

    result = pd.DataFrame()
    #for i in range(len(links)):
    for link in links:
        try:
            page = urlopen(link).read()
            data = bs(page, 'html.parser')
            body = data.find('body')
            script = body.find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')

            json_data = json.loads(raw)

            posts = json_data['entry_data']['PostPage'][0]['graphql']
            posts = json.dumps(posts)
            posts = json.loads(posts)

            x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
            x.columns = x.columns.str.replace("shortcode_media.", "")
            result = result.append(x)
        except:
            np.nan

    # Just check for the duplicates
    result = result.drop_duplicates(subset = 'shortcode')
    result.index = range(len(result.index))
    
    result.to_csv(path_or_buf="./docs/"+hashtag+"_post.csv", index=False)
    

