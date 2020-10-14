import pandas as pd

DATASET = "emails_updated_datetime.csv"


def parse_data(dataset):
    """
    Parses the <dataset>.

    Args:
        dataset (str): A file path to the dataset.

    Returns:
        df: A Pandas dataframe.
        data: A list of parsed data.
        categories: A dictionary of data, {'all': data, 'spam': data_spam, 'ham': data_ham}.
        columns: A list of column headers.
    """
    # Parse dataset into pandas dataframe
    df = pd.read_csv(dataset, encoding="ISO-8859-1",
                    converters={i: str for i in range(0, 100)})
    # reorganize columns
    df = df[['Datetime', 'Spam', 'Label', 'Relevance', 'Text']]

    # convert dataframe into a list of dict
    data = df.to_dict('records')
    
    # list of dictionaries containing spam email
    data_spam = [item for item in data if item['Spam'] == '1']
    # list of dictionaries containing non-spam email
    data_ham = [item for item in data if item['Spam'] == '0']

    categories = {
        'all': data,
        'spam': data_spam,
        'ham': data_ham
    }

    # Convert to verbose data, 1 --> Spam, 0 --> Not Spam
    for row in data:
        row['Spam'] = 'Spam' if row['Spam'] == '1' else 'Not Spam'
    columns = [{"name": i, "id": i} for i in df.columns]

    return df, data, categories, columns


def export_data(data_dict=None ,dataframe=None, col=None):

    # either dictionary or dataframe must be present
    if data_dict is None and dataframe is None:
        return

    # if choose to use dataframe, data_dict will not be in use
    if dataframe:
        dictionary = None
        return dataframe.to_csv(None, encoding="ISO-8859-1")

    # if choose to use custom dict, convert to dataframe before exporting
    if data_dict:
        # allows reorganization of columns
        if col:
            dataframe = pd.DataFrame(data_dict, columns=col)
        else:
            dataframe = pd.DataFrame(data_dict)

        return dataframe.to_csv(None, encoding="ISO-8859-1")
