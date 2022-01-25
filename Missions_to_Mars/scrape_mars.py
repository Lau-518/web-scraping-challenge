# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

# Setting up mongo database

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

def scrape():



    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # # NASA Mars News



    url = 'https://redplanetscience.com/'
    browser.visit(url)



    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    news_title_1 = soup.find_all('div', class_='content_title')
    news_p_1 = soup.find_all('div', class_='article_teaser_body')


    news_title = news_title_1[0]
    news_p = news_p_1[0]




    # # JPL Mars Space Images - Featured Image


    url_2 = 'https://spaceimages-mars.com/'
    browser.visit(url_2)



    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('img', class_='headerimage')["src"]
    featured_image_url = "https://spaceimages-mars.com/" + image


    # # Mars Facts


    import pandas as pd



    url3 = 'https://galaxyfacts-mars.com/'



    tables = pd.read_html(url3)
    tables



    #Converting MARS data into a dataframe

    table_df = tables[1]
    table_df.head()


    # # Mars Hemispheres


    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)



    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')




    titles = soup.find_all("h3")
    for title in titles:
        browser.links.find_by_partial_text("Hemisphere")
            
    print(titles)



    results = soup.find_all("div", class_="description")
    
    hemisphere_image_urls=[]
    for result in results:
        link = result.find('a')
        href = link['href']
        title = link.text.strip()
        browser.visit(url4)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        pic = soup.find('img', class_='thumb')
        pic_href = url4 + pic['src']
        hemisphere_image_urls.append({"title":title,"img_url":pic_href})
    print(hemisphere_image_urls)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "pic_href":pic_href,
        "table": table_df,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results

    return mars_data





