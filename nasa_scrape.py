from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
import time 

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    nasa_data = {}
    
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_classes = soup.find('div', class_="content_title")
    titles = title_classes.find('a').text
    
    outer = soup.find('div', class_="rollover_description")
    inner = outer.find('div', class_="rollover_description_inner").text
    
    nasa_data['News_Title'] = titles
    nasa_data['Description'] = inner

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response_twitter = requests.get(twitter_url)
    twitter_soup = BeautifulSoup(response_twitter.text, 'html.parser')
    
    weather_tweet = twitter_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    nasa_data['Weather'] = weather_tweet
    
    url_for_splinter = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_for_splinter)

    splinter_html = browser.html
    splinter_soup = BeautifulSoup(splinter_html, 'html.parser')
    
    image = splinter_soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image
    
    
    astrogeology = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeology)
    
    astro_html = browser.html
    astro_soup = BeautifulSoup(html, 'html.parser')
    image_scrape = astro_soup.find_all("img")
    
    hemisphere = []
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        astro_loop_soup = BeautifulSoup(html, 'html.parser')

        image_source = astro_loop_soup.find("img", class_="wide-image")["src"]
        image_title = astro_loop_soup.find("h2",class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+ image_source
        hemisphere_image_urls={"title":image_title,"img_url":image_url}
        browser.back()
    
    nasa_data['Hemisphere'] = hemisphere
    