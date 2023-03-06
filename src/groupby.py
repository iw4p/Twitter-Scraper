import pandas as pd
import json

def most_mentioned(username: str):
    username = './replies/' + username + '.csv'
    df = pd.read_csv(username, index_col=False)
    list_of_columns_index = [2]
    df = df[[df.columns[i] for i in list_of_columns_index]]
    df.columns =['id']
    df = df.groupby('id').size().reset_index()
    df.columns =['id', 'count']
    df = df.sort_values(by=['count'], ascending = False)
    df = df.drop_duplicates(subset=['id'], keep='first',inplace=False)
    df = df[df['id'] != '[empty]']

    return json.loads(df.to_json(orient='records'))
