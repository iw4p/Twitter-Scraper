import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv('alikarimi_ak8.csv')
    list_of_columns_index = [2]
    df = df[[df.columns[i] for i in list_of_columns_index]]
    df.columns =['id']
    df2 = df.groupby('id').value_counts()
    print(df2)

