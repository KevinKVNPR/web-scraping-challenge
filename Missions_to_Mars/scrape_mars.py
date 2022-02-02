from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import pandas as pd
import os
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
# init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
  # browser = init_browser()

    mars_dict = {}

#Latest News
    url_latest_news = 'https://redplanetscience.com/'
    browser.visit(url_latest_news)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(2)
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    print(news_title)
    print("--------------------------------------------------------------------")
    print(news_p)

    #Featured Image
    space_images_url =  'https://spaceimages-mars.com/'
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    html = browser.html
    images_soup = bs(html, 'html.parser')
    image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = space_images_url + image_path
    print(featured_image_url)

    #Mars Facts
    galaxy_facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(galaxy_facts_url)
    mars_facts_df = tables[1]
    mars_facts_df.columns = ["Description", "Value"]
    mars_html_table_string = mars_facts_df.to_html()
    mars_html_table_string
    mars_html_table_string.replace('\n', '')
    print(mars_html_table_string)

    #Hemispheres
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    mars_hemispheres = hemispheres_soup.find_all('div', class_="item")
    hemisphere_image_data = []

    for hemisphere in range(len(mars_hemispheres)):

        hemis_title = browser.find_by_css("a.product-item h3")
        hemis_title[hemisphere].click()
        time.sleep(1)
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        base_url = 'https://marshemispheres.com/'
        hemis_url = img_soup.find('img', class_="wide-image")['src']
        img_url = base_url + hemis_url
        img_title = browser.find_by_css('.title').text
        hemisphere_image_data.append({"title": img_title,
                                "img_url": img_url})
        browser.back()

    browser.quit()

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table_string),
        "hemisphere_images": hemisphere_image_data
    }

    return mars_dict