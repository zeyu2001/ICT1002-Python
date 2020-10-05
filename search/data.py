import pandas as pd

DATASET = "emails_updated.csv"
DEFAULT_PATH = "C:\\Program Files (x86)\\SpamDetector"
DEFAULT_FILENAME = "export.csv"

def parse_data(dataset):
    # Parse dataset into pandas dataframe
    df = pd.read_csv(dataset, encoding="ISO-8859-1",
                    converters={i: str for i in range(0, 100)})
    # reorganize columns
    df = df[['Spam', 'Label', 'Relevance', 'Text']]

    #convert dataframe into a list of dict
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


def export_data(data_dict=None ,dataframe=None ,path=DEFAULT_PATH, filename=DEFAULT_FILENAME, col=None):
    # ensure there is a path to store exported file
    fullpath = path + '\\' + filename

    # either dictionary or dataframe must be present
    if data_dict is None and dataframe is None:
        return

    # if choose to use dataframe, data_dict will not be in use
    if dataframe:
        dictionary = None
        dataframe.to_csv(fullpath, encoding="ISO-8859-1")
        return

    # if choose to use custom dict, convert to dataframe before exporting
    if data_dict:
        # allows reorganization of columns
        if col:
            dataframe = pd.DataFrame(data_dict, columns=col)
        else:
            dataframe = pd.DataFrame(data_dict)

        dataframe.to_csv(fullpath, encoding="ISO-8859-1")
        return
