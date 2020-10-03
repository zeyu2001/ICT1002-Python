import pandas as pd

DATASET = "emails_updated.csv"

# Parse dataset into pandas dataframe
df = pd.read_csv(DATASET, encoding="ISO-8859-1",
                 converters={i: str for i in range(0, 100)})
df = df[['Spam', 'Label', 'Relevance', 'Text']]
DATA = df.to_dict('records')
DATA_SPAM = [item for item in DATA if item['Spam'] == '1']
DATA_HAM = [item for item in DATA if item['Spam'] == '0']

CATEGORIES = {
    'all': DATA,
    'spam': DATA_SPAM,
    'ham': DATA_HAM
}

# Convert to verbose data, 1 --> Spam, 0 --> Not Spam
for row in DATA:
    row['Spam'] = 'Spam' if row['Spam'] == '1' else 'Not Spam'
COLUMNS = [{"name": i, "id": i} for i in df.columns]
