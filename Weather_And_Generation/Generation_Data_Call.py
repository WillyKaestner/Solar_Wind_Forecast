"""
Electricity generation data classes and functions to load and prepare weather data for further use
"""

import pandas as pd
from dataclasses import dataclass
from selenium import webdriver
import time
from pathlib import Path

@dataclass
class SmardGenerationData:
    """Overall electricity generation class for generation data from smard.de """
    start_date: str
    end_date: str
    regelzone: str  # ToDo: Dict oder Liste einführen damit man keine Schreibfehler machen kann

    def load_generation_data_from_smard_and_save_as_csv(self):
        # ToDO: Nicht vergessen, dass die Erzeugungsdaten auf smard in UTC+1 zu finden sind -> deshalb zu start_date & end_data puffer einplanen
        # Pfad zum Chromedriver
        PATH = r"C:\Program Files (x86)\chromedriver_94_0_4606_61.exe"

        # Default Download-pfad für Dateien im Chrome Browser Object ändern
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": r"C:\Users\Willy\OneDrive - bwedu\_Willy_\10_Python\Solar_Wind_Forecast\data\02_Forecast_Validation_Data"}
        options.add_experimental_option("prefs", prefs)

        # Webdriver starten mit definierten optionen
        driver = webdriver.Chrome(executable_path=PATH, options=options)

        unix_start = str(self.time_to_unix(self.start_date)) + "LetzteZiffer4Mal"  # ToDo: List comprehension verwenden
        unix_end = str(self.time_to_unix(self.start_date)) + "LetzteZiffer4Mal"  # ToDo: List comprehension verwenden
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
    def time_to_unix():
        pass


if __name__ == "__main__":
    generation_bw = SmardGenerationData(start_date="28Sep2020",
                                        end_date="19Sep2021",
                                        regelzone="bw").read_generation_data_from_file("01_Base_Data/Realisierte_Erzeugung_202009270000_202109202359.csv")
