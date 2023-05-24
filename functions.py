#import libraries
import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.metrics import confusion_matrix, plot_confusion_matrix

artifact_cols = ['id', 'funder', 'recorded_by', 'region', 'wpt_name',
                'payment', 'payment_type', 'source_type', 'source_class',
                'water_quality', 'waterpoint_type_group', 'quantity_group', 'extraction_type',
                'extraction_type_group', 'num_private', 'management', 'public_meeting']

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

# convert target column for binary classification
def ternary_to_binary(data, target='status_group'):
    """
    Changes target values such that it fits a binary classification problem
    Params: pandas.DataFrame, target(pamdas.Series)
    Returns: pandas.DataFrame(target transformed)
    """
    data[target] = data[target].replace(['functional needs repair', 'non functional'], 'needs_repair')
    return data


#calculate age 
def calculate_age(data, date_col='date_recorded', year_col='construction_year'):
    """
    Calculate age from 'construction_year'  and 'date_recorded'
    Params:pandas.DataFrame
    Returns: pandas.DataFrame
    """
    # Convert the date column to datetime format
    data[date_col] = pd.to_datetime(data[date_col])
    # Extract the year from the date column
    data[date_col + '_year'] = data[date_col].dt.year
    # Calculate the age column as the date column year - construction year
    data['age'] =  data[date_col + '_year'] - data[year_col]
    # Drop the original date column and the date column year
    data.drop(columns=[date_col, date_col + '_year'], inplace=True)
    return data


#model evaluation
def cross_val_evaluate(pipe, X, y):
    """
    Cross validate using given pipeline and print scores and evaluate model
    Params: pipeline, X, y
    """
    scoring = ['accuracy', 'recall']
    #cross validate pipeline
    result = cross_validate(pipe, X, y, 
                            return_train_score=True, scoring=scoring)
    
    print(result['train_accuracy'])
    print('Train Accuracy', result['train_accuracy'].mean())
    print('\n')
    print(result['test_accuracy'])
    print('Cross-Validation Accuracy', result['test_accuracy'].mean())
    print('\n')
    print('Training Recall:', result['train_recall'].mean())
    print('Test Recall:', result['test_recall'].mean())
    #confusion martix
    plot_confusion_matrix(pipe, X, y, normalize='true')

