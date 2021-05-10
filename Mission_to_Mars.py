# setup libraries
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# visit mars news site
url = 'https://redplanetscience.com'
browser.visit(url)
browser.is_element_not_present_by_css('div.list_text', wait_time=1)

# convert browser html to soup and quit
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_ = 'content_title')


news_title = slide_elem.find('div', class_ = 'content_title').get_text()
news_title


news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
news_p


# ## Featured Images

# visit url
url = 'https://spaceimages-mars.com'
browser.visit(url)

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parse resulting html w/ soup
html = browser.html
img_soup = soup(html, 'html.parser')

img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

browser.quit()





