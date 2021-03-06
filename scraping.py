# setup libraries
from splinter import Browser, browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
#set up splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data


def mars_news(browser):
# visit mars news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_not_present_by_css('div.list_text', wait_time=1)

    # convert browser html to soup and quit
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_ = 'content_title').get_text()
        news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
    except AttributeError:
        return None
    return news_title, news_p


# ## Featured Images
def featured_image(browser):
    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # parse resulting html w/ soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    print(scrape_all())





