import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from joblib import dump

#%%

"""
01 LOAD & SELECT DATA
"""
# Read the data
X_solar_full = pd.read_pickle("data/train_solar.pkl")

# Delete the detailed weather description columns since we have to many different unique object values which will throw an error we have
# description values in our validation or test datasets which didn't occur in our training dataset.
X_solar_full.drop(columns=["STG_weather.description", "FRB_weather.description", "MAN_weather.description", "RAV_weather.description"],
                  inplace=True)

# Select only rows where the weather.main description is on of the following : ['Clouds', 'Clear', 'Rain', 'Fog', 'Drizzle', 'Mist', 'Snow']
weather_main = ['Clouds', 'Clear', 'Rain', 'Fog', 'Drizzle', 'Mist', 'Snow']
X_solar_full = X_solar_full[(X_solar_full["STG_weather.main"].isin(weather_main)) &
                            (X_solar_full["FRB_weather.main"].isin(weather_main)) &
                            (X_solar_full["MAN_weather.main"].isin(weather_main)) &
                            (X_solar_full["RAV_weather.main"].isin(weather_main))]

"""
02 DATA PREPARATION
"""
# Separate target from predictors
y_solar = X_solar_full["PV[MWh]"]
X_solar_full.drop(["PV[MWh]"], axis=1, inplace=True)

# Break off validation set from training data -> random_state=1 delivers an training dataset with all seven values in
# the four different weather.main columns
X_train, X_valid, y_train, y_valid = train_test_split(X_solar_full, y_solar, train_size=0.8, test_size=0.2, random_state=1)

# Select categorical columns with relatively low cardinality (convenient but arbitrary)
categorical_cols = [cname for cname in X_train.columns if
                    X_train[cname].dtype == "object"]

# Select numerical columns
numerical_cols = [cname for cname in X_train.columns if
                  X_train[cname].dtype in ['int64', 'float64']]

#%%
"""
03 PIPELINE (IMPUTATION AND MODEL)
"""

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model', model)])

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = clf.predict(X_valid)

print('MAE:', mean_absolute_error(y_valid, preds))

#%% Gegenüberstellung der Vorhersage und der Ausgangsdaten
Solar_Vergleich = pd.DataFrame()
Solar_Vergleich["Base_PV[MWh]"] = y_valid.reset_index(drop=True)
Solar_Vergleich["Predict_PV[MWh]"] = preds

#%% Export model
dump(clf, 'data/solar_model.joblib')

#%% Export X_valid
pd.to_pickle(X_valid, "data/X_valid_solar.pkl")
