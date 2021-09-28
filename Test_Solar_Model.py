import pandas as pd
from joblib import load

clf = load("data/solar_model.joblib")
X_valid = pd.read_pickle("data/X_valid_solar.pkl")

#%%
preds = clf.predict(X_valid)