import pandas as pd

DATASET = "emails_updated.csv"

def parse_data(dataset):
    # Parse dataset into pandas dataframe
    df = pd.read_csv(dataset, encoding="ISO-8859-1",
                    converters={i: str for i in range(0, 100)})
    df = df[['Spam', 'Label', 'Relevance', 'Text']]
    data = df.to_dict('records')
    data_spam = [item for item in data if item['Spam'] == '1']
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
