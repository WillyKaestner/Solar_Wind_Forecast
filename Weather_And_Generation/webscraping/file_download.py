#%%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


# function to take care of downloading file
def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\Willy\Downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome(options=chrome_options, executable_path="C:\Program Files (x86)\chromedriver_94_0_4606_61.exe")

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = r"C:\Users\Willy\OneDrive - bwedu\_Willy_\10_Python\Solar_Wind_Forecast\data\02_Forecast_Validation_Data"

# function to handle setting up headless download
enable_download_headless(driver, download_dir)

# get request to target the site selenium is active on
Gebiet = ["50Hertz", "DE", "TransnetBW"]
smard = f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:1,%22selectedSubCategory%22:1,%22selectedRegion%22:%22{Gebiet[0]}%22,%22from%22:1631484000000,%22to%22:1632434399999,%22selectedFileType%22:%22CSV%22%7D"
driver.get(smard)

# buttons = driver.find_elements_by_tag_name("button")
# nr = 0
# for button in buttons:
#     print(f"Button Nr{nr} - " + button.text)
#     nr = nr+1
#
# buttons[15].click()
# get request to target the site selenium is active on
# driver.get("https://www.thinkbroadband.com/download")

#%%
# initialize an object to the location on the html page and click on it to download
# search_input = driver.find_element_by_css_selector('#main-col > div > div > div:nth-child(8) > p:nth-child(1) > a > img')
twitter_button = "/html[@class=' ']/body[@id='top']/main[@id='page-content']/div[@class='c-article c-article--grow']/header[@class='c-article__header']/nav[@class='c-article-menu l-no-print js-article-menu is-open']/div[@id='more-btn']/ul[@class='c-article-menu__list']/li[@class='c-article-menu__element'][1]/ul[@class='c-article-menu-actions']/li[@class='c-article-menu-actions__item'][1]/button[@class='c-article-menu-actions__item-link icon-twitter js-share-twitter']"
download_button_xpath = "/html[@class=' ']/body[@id='top']/main[@id='page-content']/div[@class='c-article c-article--grow']/div[@class='c-article__content']/div[@class='c-download-list']/download/div[@class='c-download-filter']/div"
download_button_xpath_relativ = "//div[@id='help-download']"
download_button = driver.find_element_by_xpath(download_button_xpath_relativ)
# download_button_css = driver.find_element_by_css_selector("div.c-download-filter")
# print(download_button_css.id)

# search_input = driver.find_element_by_tag_name("download")
# print(search_input.tag_name)
# buttons = search_input.find_element_by_tag_name("button")
# # search_input.click()
# for object in download_button_css:
#     print(object.text)
