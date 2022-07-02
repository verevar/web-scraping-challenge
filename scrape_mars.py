from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    time.sleep(1)

    #mars news

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title=soup.find("div",class_='content_title').text

    news_p=soup.find("div",class_='article_teaser_body').text

    #JPL Mars Space Images

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    stuff=soup.find('div',class_='carousel_container')

    image=stuff.a["data-fancybox-href"]

    url="https://www.jpl.nasa.gov/"

    featured_image_url = url + image

    #Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en&lang=en&lang=en'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather=soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    #Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    html=browser.html
    soup=bs(html, 'html.parser')
 
    tables = pd.read_html(facts_url)

    mars_df=tables[1]
    mars_df.columns=["description","value"]
    mars_df.set_index("description",inplace=True)

    mars_html_table=mars_df.to_html()
    mars_html_table.replace('\n','')
    

    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    all_hemi1=soup.find("div",class_='collapsible results')

    hemisphere1=all_hemi1.find_all('a')

    hemisphere_image_urls=[]

    for hemi in hemisphere1:
        if hemi.h3:
            title=hemi.h3.text
            link=hemi["href"]
            main_url="https://astrogeology.usgs.gov/"
            forward_url=main_url+link
            browser.visit(forward_url)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemi2=soup.find("div",class_= "downloads")
            image=hemi2.ul.a["href"]
            hemi_dict={}
            hemi_dict["title"]=title
            hemi_dict["img_url"]=image
            hemisphere_image_urls.append(hemi_dict)
            browser.back()


    mars_py_dict={
        "mars_news_title": news_title,
        "mars_news_paragraph": news_p,
        "featured_mars_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_html_table,
        "mars_hemisphers": hemisphere_image_urls
    }
    browser.quit()

    return mars_py_dict 