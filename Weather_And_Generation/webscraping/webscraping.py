#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver = webdriver.Chrome(ChromeDriverManager().install())
"""
01 Configure chromedriver
"""
PATH = "C:\Program Files (x86)\chromedriver_94_0_4606_61.exe"

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": r"C:\Users\Willy\OneDrive - bwedu\_Willy_\10_Python\Solar_Wind_Forecast\data\02_Forecast_Validation_Data"}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(PATH, options=options)

"""
02 Smard
"""
Gebiet = ["50Hertz", "DE", "TransnetBW"]
smard = f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:1,%22selectedSubCategory%22:1,%22selectedRegion%22:%22{Gebiet[2]}%22,%22from%22:1631484000000,%22to%22:1632434399999,%22selectedFileType%22:%22CSV%22%7D"

"""
03 Tectwithtim
"""
techwithtim = "https://techwithtim.net"


driver.get(smard)
print(driver.title)

buttons = driver.find_elements_by_tag_name("button")
# nr = 0
# for button in buttons:
#     print(f"Button Nr{nr} - " + button.text)
#     nr = nr+1
#     time.sleep(2)
buttons[15].click()

time.sleep(5)
driver.quit()



#%%
# print(driver.title)
# # Find search box
# search = driver.find_element_by_name("s")
# # type in test in search field
# search.send_keys("test")
# # press Enter key
# search.send_keys(Keys.RETURN)
#
# try:
#     main = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "main"))
#     )
#     # print(main.text)
#
#     articles = main.find_elements_by_tag_name("article")
#     for article in articles:
#         header = article.find_element_by_class_name("entry-summary")
#         print(header.text)
#
# finally:
#     driver.quit()
#
# # main = driver.find_element_by_id("main")
#
#
# # time.sleep(5)
#
# driver.quit()
