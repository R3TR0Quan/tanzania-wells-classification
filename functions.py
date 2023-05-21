#import libraries
import pandas as pd

artifact_cols = ['funder', 'installer', 'recorded_by', 'region',
                'payment', 'payment_type', 'source_type', 'source_class',
                'water_quality', 'waterpoint_type_group', 'quantity_group']

#initialize empty df
df = pd.DataFrame()

#drop irrelevant columns
def del_irrelevant_cols(data):
    """
    Drops the columns specified as they are irrelevant data artifacts

    Parameters:
        data: the dataframe, train or test

    Returns:
        pandas.Datafrmae without irrelevant columns
    """
    df = data.drop(artifact_cols, axis=1)
    return df

#drop columns with too many missing vals
"""
Drops columns with missing values past threshold

Parameters:
    data: the dataframe, train or test
    thresh: (float) percentage of acceptable missing values

Returns:
    pandas.DataFrame w\o columns with too many missing vals
"""
def drop_near_empty_cols(data, thresh=.2):
    #loop through columns
    for col in data.columns:
        pass

