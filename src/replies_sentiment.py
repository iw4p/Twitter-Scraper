import pandas as pd
from textblob import TextBlob
import json
# from translate_fa_to_en import translate

def sentiment_analysis(username: str):
    full_path = './replies/' + username + '.csv'
    df = pd.read_csv(full_path)
    df.columns = ['date', 'name', 'id', 'text', 'target']

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
    df = df.dropna()
    sentiment_counts = df.groupby(['analysis']).size()
    df = json.loads(df.to_json(orient='records'))

    # visualize the sentiments 
    # fig = plt.figure(figsize=(6,6), dpi=100)
    # ax = plt.subplot(111)
    # sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")

    return df