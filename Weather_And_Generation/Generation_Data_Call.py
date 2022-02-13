"""
Electricity generation data classes and functions to load and prepare electricity data for further use
"""

from Weather_And_Generation.constants import REGELZONEN

import pandas as pd
from dataclasses import dataclass
from selenium import webdriver
import time
from pathlib import Path
from datetime import datetime

@dataclass
class SmardGenerationData:
    """Overall electricity generation class for generation data from smard.de """
    start_date: str
    end_date: str
    regelzone: str

    def load_generation_data_from_smard_and_save_as_csv(self):
        # Pfad zum Chromedriver
        PATH = r"C:\Program Files (x86)\chromedriver_96_0_4664_45.exe"

        # Default Download-pfad für Dateien im Chrome Browser Object ändern
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": r"C:\Users\Willy\OneDrive - bwedu\_Willy_\10_Python\Solar_Wind_Forecast\data\02_Forecast_Validation_Data"}
        options.add_experimental_option("prefs", prefs)

        # Webdriver starten mit definierten optionen
        driver = webdriver.Chrome(executable_path=PATH, options=options)

        unix_start = str(self.adjust_date(self.start_date))
        unix_end = str(self.adjust_date(self.end_date))
        smard = f"https://www.smard.de/home/downloadcenter/download-marktdaten#!?downloadAttributes=%7B%22selectedCategory%22:1,%22selectedSubCategory%22:1," \
                f"%22selectedRegion%22:%22{self.regelzone}%22,%22from%22:{unix_start},%22to%22:{unix_end},%22selectedFileType%22:%22CSV%22%7D"

        driver.get(smard)
        download_button = driver.find_element_by_id("help-download")
        download_button.click()
        # Wait 5 seconds so download is finished
        time.sleep(5)
        driver.quit()

    def read_generation_data_from_file(self, data_filepath: str) -> pd.DataFrame:
        """Load generation data from CSV file and resample data to hourly UTC values"""
        base_path = Path(__file__).parent
        file_path = (base_path / f"../data/{data_filepath}").resolve()
        generation = pd.read_csv(file_path, sep=";")

        # Aus den Datum und Uhrzeit Spalten die Strings nehmen und Datetime Index erstellen
        generation["Datum_UTC+1"] = generation[["Datum", "Uhrzeit"]].agg(" ".join, axis=1)
        generation["Datum_UTC+1"] = pd.to_datetime(generation["Datum_UTC+1"], format='%d.%m.%Y %H:%M')
        generation.drop(columns=["Datum", "Uhrzeit"], inplace=True)

        # Datum als Index setzen und mittels resample von 0,25h auf 1h Auflösung aggregieren
        generation.set_index("Datum_UTC+1", inplace=True)
        generation_hourly = generation.resample('H').sum()

        # Zeit um eine Stunde nach hinten verschieben aufgrund der UTC+1 Zeitzone
        # -> https://towardsdatascience.com/all-the-pandas-shift-you-should-know-for-data-analysis-791c1692b5e
        # Auswahl der Erzeugungsdaten für den Zeitraum in dem wir auch historische Wetterdaten zur Verfügung haben
        generation_hourly_UTC = generation_hourly.shift(periods=-1, freq='H')
        generation_hourly_UTC_Datumsauswahl = generation_hourly_UTC.loc[f"{self.start_date}":f"{self.end_date}"]

        return generation_hourly_UTC_Datumsauswahl

    def save_generation_data_as_pickle(self, generation_dataframe: pd.DataFrame) -> None:
        """Export des Dataframes als Pickle"""
        pd.to_pickle(generation_dataframe, f"../data/01_Base_Data/history_erzeugung_{self.regelzone}_{self.start_date}_{self.end_date}.pkl")

    @staticmethod
    def adjust_date(date_str) -> int:
        # Convert UTC+1 Date to Unix timestamp
        date_utc1 = datetime.strptime(date_str, "%d%b%Y")
        epoch = datetime(1970, 1, 1)
        date_unix = int((date_utc1 - epoch).total_seconds()) + 3600

        # Add last four digits to the Unix Value for Smard Website
        date_unix_str = str(date_unix)
        date_unix_str = date_unix_str + date_unix_str[-1] * 3

        return date_unix_str


if __name__ == "__main__":
    # generation_bw = SmardGenerationData(start_date="28Sep2020",
    #                                     end_date="19Sep2021",
    #                                     regelzone=REGELZONEN[1]).read_generation_data_from_file("01_Base_Data/Realisierte_Erzeugung_202009270000_202109202359.csv")

    generation_bw = SmardGenerationData(start_date="28Sep2021",
                                        end_date="30Sep2021",
                                        regelzone=REGELZONEN[1])

    generation_bw.load_generation_data_from_smard_and_save_as_csv()

    # erzeugung_bw = generation_bw.read_generation_data_from_file("02_Forecast_Validation_Data/Realisierte_Erzeugung_202109280000_202109282359.csv")
