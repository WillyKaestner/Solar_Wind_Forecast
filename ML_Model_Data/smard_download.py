#%%
from selenium import webdriver
import time

"""
01 Configure chromedriver
"""
# Pfad zum Chromedriver
PATH = "C:\Program Files (x86)\chromedriver_94_0_4606_61.exe"

# Default Download-pfad für Dateien im Chrome Browser Object ändern
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": r"C:\Users\Willy\OneDrive - bwedu\_Willy_\10_Python\Solar_Wind_Forecast\data\02_Forecast_Validation_Data"}
options.add_experimental_option("prefs", prefs)

# Webdriver starten mit definierten optionen
driver = webdriver.Chrome(executable_path=PATH, options=options)

"""
02 Smard Download
"""
Gebiet = ["50Hertz", "DE", "TransnetBW"]
smard = f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:1,%22selectedSubCategory%22:1," \
        f"%22selectedRegion%22:%22{Gebiet[2]}%22,%22from%22:1631484000000,%22to%22:1632434399999,%22selectedFileType%22:%22CSV%22%7D"

driver.get(smard)
download_button = driver.find_element_by_id("help-download")
download_button.click()
# Wait 5 seconds so download is finished
time.sleep(5)
driver.quit()
