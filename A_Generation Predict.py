"""
Predict PV and Wind Generation for the next 48 hours in Baden-Württemberg based on the weather forecast
from Stuttgart, Freiburg, Mannheim and Ravensburg
"""

from Predict.A1_Solar_Predict import solar_predict
from Predict.A2_Wind_Predict import wind_predict

if __name__ == "__main__":
    solar_predict()
    wind_predict()
