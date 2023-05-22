#import libraries
import pandas as pd

artifact_cols = ['id', 'funder', 'recorded_by', 'region', 'wpt_name',
                'payment', 'payment_type', 'source_type', 'source_class',
                'water_quality', 'waterpoint_type_group', 'quantity_group', 'extraction_type',
                'extraction_type_group', 'num_private']

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
def drop_nulls(data, thresh=.1):
    #loop through columns
    for col in data.columns:
        if((data[col].isna().sum()/len(data[col]) > thresh)):
            data = data.drop(col, axis=1)
        else:
            continue
    data = data.dropna()
    return data

#combined drop artifact cols and nulls
def drop_artefacts_and_nulls(data, thresh=.1):
    """
    Drops artefact features; drops columns with null values >10% and drops null rows
    Params:panda.DataFrame
    Returns:pandas.DataFrame(transformed)
    """
    data = del_irrelevant_cols(data)
    data = drop_nulls(data, thresh=thresh)
    return data