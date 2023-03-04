import pandas as pd
from textblob import TextBlob

df = pd.read_csv('./replies/testobama.csv')
df.columns = ['date', 'name', 'id', 'text', 'target']

def sentiment_analysis(df):

    def getSubjectivity(text):
        try:
            return TextBlob(text).sentiment.subjectivity
        except:
            return None

    def getPolarity(text):
        try:
            return TextBlob(text).sentiment.polarity
        except:
            return None
        
    df['subjectivity'] = df['text'].apply(getSubjectivity)
    df['polarity'] = df['text'].apply(getPolarity)

    def getAnalysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'
    df['analysis'] = df['polarity'].apply(getAnalysis)
    return df


sentiment_analysis(df)

# print(df.head())
# df.to_csv('out.csv')  
