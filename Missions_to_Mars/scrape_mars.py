from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_all():
    mars_nasa = scrape_info()
    mars_pic = picture()
    mars_twitter = twitter()
    mars_facts = data_table()

    nasa_data = {
        "title": mars_nasa[0],
        "para": mars_nasa[1],
        "picture": mars_pic,
        "weather": mars_twitter,
        "facts": mars_facts
    }

    return nasa_data

def scrape_info():
    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # getting nasa news
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    # Store data in a dictionary
    #nasa_data = {
      # "title": news_title,
      # "para": news_p    
     #  }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return news_title, news_p

def picture():
    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)
    #drill into webpage
    click_im = browser.find_by_id('full_image')
    click_im.click()

    time.sleep(2)
    #drill in to other website to get image link
    enhance_pic = browser.find_link_by_partial_text('more info')
    enhance_pic.click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # getting new url and image
    img_url = "https://www.jpl.nasa.gov/"
    relative_image_path = soup.select_one("figure.lede a img").get("src")
    featured_image_url = img_url + relative_image_path

    # Store data in a dictionary
    picture_data = {
       "picture": featured_image_url
       }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return picture_data

def twitter():
    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # getting nasa news
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Store data in a dictionary
    weather_data = {
       "weather": mars_weather
       }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return weather_data

def data_table():
    #pulling in url
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    #converting to dataframe
    df = tables[0]
    df.columns = ['Data','Values']
    df = df.set_index("Data")

    #writing to html
    html_table = df.to_html()

    return html_table
