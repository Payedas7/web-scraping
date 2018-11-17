import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser

import numpy as np
import pandas as pd
import pymongo
from datetime import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def get_new_mars_article():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url_1 = 'https://mars.nasa.gov/news/'
    browser.visit(url_1)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the latest Mars news.
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    #print(news_title)
    #print(news_p)
  
    # Add the news date, title and summary to the dictionary
    
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p
    browser.quit()
    return news_title,news_p

    # ## JPL Mars Space Images - Featured Image
    # ------
    # - Visit the url for JPL's Featured Space [Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # - Use splinter to navigate the site and find the full size jpg image url for the current Featured Mars Image.
    # - Save a complete url string for this image


    # While chromedriver is open go to JPL's Featured Space Image page. 
def get_featured_image_url():    
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Save the image url to a variable called `featured_image_url`
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    featured_image_url
    
    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url
    browser.quit()
    return featured_image_url

    # ## Mars Weather 
    # ------
    # - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the             latest Mars weather tweet from the page.
    # - Save the tweet text for the weather report.
def get_mars_weather():    
    url_3  = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_3)
    # Scrape the browser into soup and use soup     
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Save the tweet text for the weather report as a variable called `mars_weather`.
    mars_weather = soup.find("p", "TweetTextSize").string
    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather
    browser.quit()
    return mars_weather
    # ## Mars Facts
    # ------
    # -  Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    # - Use Pandas to convert the data to a HTML table string.
def get_mars_facts():
    url_4 = "https://space-facts.com/mars/"
    browser.visit(url_4)
    # Scrape the browser into soup and use soup     
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    list_category = []

    categories = soup.find_all("td", "column-1")

    for item in categories:
        
    #print(item.string)
        list_category.append(item.string)
    list_category    

    list_facts = []

    facts = soup.find_all("td", "column-2")

    for item in facts:
    #print(item.text)
        list_facts.append(item.text.rstrip('\n'))
    
    list_facts
    mars_facts_1 = pd.DataFrame({"description": list_category, "values": list_facts})
    mars_facts=mars_facts_1.set_index("description")
    
    marsinformation = mars_facts.to_html(classes='marsinformation', index=False, col_space=500, escape=False)
    # Add the Mars facts table to the dictionary
    mars_data["mars_facts"] = marsinformation
    browser.quit()
    return marsinformation

    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
def get_hemisphere_images():    
    browser = init_browser()
    url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_5)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls=[]

    
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    # Return the dictionary
    return hemisphere_image_urls
