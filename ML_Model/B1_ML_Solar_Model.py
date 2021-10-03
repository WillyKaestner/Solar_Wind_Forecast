"""
Random Forest ML Model für die Solarerzeugung in Baden-Württemberg
"""

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
def solar_model():
    """
    01 LOAD & SELECT DATA
    """
    # Read the data
    X_solar_full = pd.read_pickle("../data/train_solar.pkl")

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

    """
    04 CALC BEST N_ESTIMATORS
    """
    # def get_mae(n_estimators, train_X, val_X, train_y, val_y):
    #     model = RandomForestRegressor(n_estimators=n_estimators, random_state=0)
    #     clf = Pipeline(steps=[('preprocessor', preprocessor),
    #                           ('model', model)])
    #     clf.fit(train_X, train_y)
    #     preds_val = clf.predict(val_X)
    #     mae = mean_absolute_error(val_y, preds_val)
    #     return mae
    #
    #
    # candidate_max_leaf_nodes = [25, 50, 100, 150, 200, 250, 500]
    # # Write loop to find the ideal tree size from candidate_max_leaf_nodes
    # mae_collection = []
    #
    # for max_leaf_nodes in candidate_max_leaf_nodes:
    #     mae = get_mae(max_leaf_nodes, X_train, X_valid, y_train, y_valid)
    #     mae_collection.append([max_leaf_nodes, mae])
    #
    # mae_df = pd.DataFrame(mae_collection, columns=["max_leaf_nodes", "mae"])
    #
    # # Store the best value of n_estimators
    # best_n_estimators = mae_df.loc[mae_df["mae"].idxmin(), "max_leaf_nodes"]

    """
    05 FINAL MODEL
    """
    # Define model
    model = RandomForestRegressor(n_estimators=150, random_state=0)

    # Bundle preprocessing and modeling code in a pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('model', model)])

    # Preprocessing of training data, fit model
    clf.fit(X_train, y_train)

    # Preprocessing of validation data, get predictions
    preds = clf.predict(X_valid)

    """
    06 RESULTS AND EXPORT
    """

    print('MAE:', mean_absolute_error(y_valid, preds))

    # Gegenüberstellung der Vorhersage und der Ausgangsdaten
    Solar_Vergleich = pd.DataFrame()
    Solar_Vergleich["Base_PV[MWh]"] = y_valid.reset_index(drop=True)
    Solar_Vergleich["Predict_PV[MWh]"] = preds
    Solar_Vergleich["Diff"] = Solar_Vergleich["Base_PV[MWh]"] - Solar_Vergleich["Predict_PV[MWh]"]

    # Export model
    dump(clf, '../data/solar_model.joblib')

if __name__ == "__main__":
    solar_model()

