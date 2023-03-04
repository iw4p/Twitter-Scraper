import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv('testobama.csv')
    list_of_columns_index = [2]
    df = df[[df.columns[i] for i in list_of_columns_index]]
    df.columns =['id']
    df2 = df.groupby('id').size().reset_index()
    df2.columns =['id','count']
    df2 = df2.sort_values(by=['count'], ascending = False)
    df2 = df2.drop_duplicates(subset=['id'], keep='first',inplace=False)
    # df2 = df2.drop_duplicates(subset=['A', 'C'], keep=False)

    print(df2.head())
    

