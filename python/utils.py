import os
from sklearn.model_selection import train_test_split


def get_data_dir():
    cwd = os.path.abspath(__file__)
    dir = os.path.abspath(os.path.join(cwd, os.pardir))
    return os.path.join(dir, '..', 'data')


def split_dataset(data_frame, test_size=.5, shuffle=True, random_state=73):
    """
    Given a pandas data frame, split the data set into a test and train datasets using sklearn
    :param shuffle: Shuffles the data prior to splitting it
    :param test_size: The percentage of data which will be split in train/test
    :param random_state: A predictive state to always return the same dataset
    :param data_frame: Pandas dataframe
    :return: Tuple(train, test)
    """
    return train_test_split(data_frame, test_size=test_size, shuffle=shuffle, random_state=random_state)


def calculate_statistics(actual, predicted):
    """
    Calculates and prints the accuracy for each feature
    :param actual: The actual values
    :param predicted: The predicted values
    :return: N/A
    """
    result = {
        'hit_counts': 0 * len(actual.columns),
        'miss_counts': 0 * len(actual.columns)
    }
    for column in actual:
        for i, row_value in actual[column].iteritems():
            if row_value == predicted:
                result['hit_counts'] = result['hit_counts'] + 1
            else:
                result['miss_counts'] = result['miss_counts'] + 1
    return [result['hit_counts'][i] / result['miss_counts'] for i in range(len(actual.columns))]
