# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {"news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_images(browser)}
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_paragraph

### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    try:
        #table scraping
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #add table/df to web application
    return df.to_html(classes=["table-bordered", "table-striped", "table-hover"], header = "true", justify = "center")


def hemisphere_images(browser):
    # Visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    # Retrieve the image urls and titles for each hemisphere.
    # Parse the resulting html with soup
    html = browser.html
    imgs_soup = soup(html, 'html.parser')

    # Retrieve mars hemisphere info
    items = imgs_soup.find_all('div', class_='item')

    # Loop through mars hemisphere info to get titles and images
    for hemisphere in items:
        try:
            # Get titles
            titles = hemisphere.h3.text
            
            # Get images
            link = hemisphere.find("a")['href']
            browser.visit(url + link)
            img_html = browser.html
            imgs_hr_soup = soup(img_html, 'html.parser')
            partial_url = imgs_hr_soup.find('ul').find('li').find('a')['href']
            img_url = url + partial_url
            
            # Append the scraped information into a list of dictionaries 
            hemisphere_image_urls.append({"img_url" : img_url, "title" : titles})

        except NameError:
            return None
        
    # return a list of dictionaries with the URL string and title of each hemisphere image
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())