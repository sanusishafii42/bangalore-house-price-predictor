import json                  # For loading/saving JSON files (like data_columns.json)
import pickle                # For loading/saving model and scaler objects
import numpy as np           # For numerical operations and creating feature vectors
import pandas as pd          # For handling DataFrames (used for scaler input)
import warnings              # To suppress warnings during execution
warnings.filterwarnings('ignore')  # Ignore all warnings (not recommended for production)

__location = None            # Will hold the list of location names (for dropdown)
__data_columns = None        # Will hold the list of all feature names (columns)
__model = None               # Will hold the loaded ML model
__scaler = None              # Will hold the loaded scaler object

def get_estimated_price(location, total_sqft, size, bath):
    """
    Predicts the price of a house given location, total_sqft, size, and bath.
    """
    try:
        size_idx = __data_columns.index('size')             # Find index for 'size' in feature columns
        sqft_idx = __data_columns.index('total_sqft')       # Find index for 'total_sqft'
        bath_idx = __data_columns.index('bath')             # Find index for 'bath'
    except Exception as e:
        raise Exception("Column order mismatch: " + str(e)) # Raise error if columns are missing

    x = np.zeros(len(__data_columns))                       # Create a zero vector for all features
    x[size_idx] = size                                      # Set the size value
    x[sqft_idx] = total_sqft                                # Set the total_sqft value
    x[bath_idx] = bath                                      # Set the bath value

    # Map location input (case-insensitive) to the correct column name
    location_map = {loc.lower(): loc for loc in __data_columns[3:]} # Map lowercase location names to original
    loc_key = location.lower()                                       # Lowercase user input for matching
    if loc_key in location_map:
        loc_idx = __data_columns.index(location_map[loc_key])        # Find index for the matched location
        x[loc_idx] = 1                                              # Set the corresponding location column to 1
    elif 'other location' in __data_columns:                        # If not found, use 'other location' if available
        loc_idx = __data_columns.index('other location')
        x[loc_idx] = 1

    x_df = pd.DataFrame([x], columns=__data_columns)                # Convert to DataFrame for scaler
    x_scaled = __scaler.transform(x_df)                             # Scale the features
    return round(__model.predict(x_scaled)[0], 2)                   # Predict and round the result

def get_location_names():
    """
    Returns the list of locations for the dropdown.
    """
    return __location

def load_saved_artifact():
    """
    Loads the model, scaler, and data columns from disk.
    """
    global __location
    global __data_columns
    global __model
    global __scaler

    # Load feature columns and locations
    with open('./server/artifact/data_columns.json', 'r') as f:
        __data_columns = json.load(f)['data_column']    # Load all feature columns
        __location = __data_columns[3:]                 # Locations are all columns after the first 3

    # Load trained model
    with open('./server/artifact/bhd_model.pickle', 'rb') as f:
        __model = pickle.load(f)
    # Load scaler
    with open('./server/artifact/scaler.pickle', 'rb') as f:
        __scaler = pickle.load(f)

    print('Loading Saved Artifacts is Done...')

if __name__ == '__main__':
    # For testing: load artifacts and print sample predictions
    print('Loading Saved Artifacts is Start...')
    load_saved_artifact()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Indira Nagar', 1555, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 2000, 2, 2))