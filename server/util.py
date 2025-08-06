import json
import pickle
import numpy as np
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')

__location = None
__data_columns = None
__model = None
__scaler = None

def get_estimated_price(location, total_sqft, size, bath):
    try:
        size_idx = __data_columns.index('size')
        sqft_idx = __data_columns.index('total_sqft')
        bath_idx = __data_columns.index('bath')
    except Exception as e:
        raise Exception("Column order mismatch: " + str(e))

    x = np.zeros(len(__data_columns))
    x[size_idx] = size
    x[sqft_idx] = total_sqft
    x[bath_idx] = bath

    location_map = {loc.lower(): loc for loc in __data_columns[3:]}
    loc_key = location.lower()
    if loc_key in location_map:
        loc_idx = __data_columns.index(location_map[loc_key])
        x[loc_idx] = 1
    elif 'other location' in __data_columns:
        loc_idx = __data_columns.index('other location')
        x[loc_idx] = 1

    x_df = pd.DataFrame([x], columns=__data_columns)
    x_scaled = __scaler.transform(x_df)
    return round(__model.predict(x_scaled)[0], 2)

def get_location_names():
    return __location

def load_saved_artifact():
    global __location
    global __data_columns
    global __model
    global __scaler

    # Use absolute paths based on this file's location
    base_dir = os.path.dirname(__file__)
    columns_path = os.path.join(base_dir, 'artifact', 'data_columns.json')
    model_path = os.path.join(base_dir, 'artifact', 'bhd_model.pickle')
    scaler_path = os.path.join(base_dir, 'artifact', 'scaler.pickle')

    with open(columns_path, 'r') as f:
        __data_columns = json.load(f)['data_column']
        __location = __data_columns[3:]

    with open(model_path, 'rb') as f:
        __model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        __scaler = pickle.load(f)

    print('Loading Saved Artifacts is Done...')

if __name__ == '__main__':
    print('Loading Saved Artifacts is Start...')
    load_saved_artifact()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Indira Nagar', 1555, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 2000, 2, 2))