import pickle
import numpy as np
import pandas as pd
import tokenizer
import datetime
import matplotlib.pyplot as plt 


def create_df_old(df, desks):
    df_res = pd.DataFrame(columns={"date": "", "tf": ""}, index=[0])
    for index, row in df.iterrows():
        if row['date'] in df_res['date'].values:
            tf_dict = df_res['tf']
        else:
            tf_dict = {}
            nr = {"date":row['date'], "tf":tf_dict}
            df_res = df_res.append(nr,ignore_index=True)
        if row['news_desk'] in desks:
            words = tokenizer.clean_text_tokenize(str(row['lead_paragraph_sw_stem']))
            for w in words:
                if w in tf_dict:
                    tf_dict[w] = tf_dict[w] + 1
                else:
                    tf_dict[w] = 1
        df_update = pd.DataFrame(columns={"date": "", "tf": ""})
        df_res.loc[df_res[df_res['date'] == row['date']].index, 'tf'] = pd.Series(tf_dict)

    return df_res

def create_dict(df, desks):
    df_res = {}
    for index, row in df.iterrows():
        if row['news_desk'] in desks:
            words = tokenizer.clean_text_tokenize(str(row['lead_paragraph_sw_stem']))
            for w in words:
                if w in df_res:
                    df_res[w] = df_res[w] + 1
                else:
                    df_res[w] = 1
    df_res = sorted(df_res.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return df_res

def new_create_dict(df):
    df_res = {}
    for index, row in df.iterrows():
            words = tokenizer.clean_text_tokenize(str(row['lead_paragraph_sw_stem']))
            for w in words:
                if w in df_res:
                    df_res[w] = df_res[w] + 1
                else:
                    df_res[w] = 1
    df_res = sorted(df_res.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return df_res


def create_monthly_dict(df):
    df_res = {}
    for index, row in df.iterrows():
        date = row['date']
        month = date.month
        if df_res.get(month) is None:
            df_res[month] = {}
        tf = df_res[month]
        words = tokenizer.clean_text_tokenize(str(row['lead_paragraph_sw_stem']))
        for w in words:
            if w in tf:
                tf[w] = tf[w] + 1
            else:
                tf[w] = 1
    for k in df_res.keys():
        tf = df_res[k]
        df_res[k] = sorted(tf.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[:6]
    return df_res


def create_covid_dict(df):
    df_res = {}
    for index, row in df.iterrows():
        date = row['date']
        if df_res.get(date) is None:
            df_res[date] = 0
        count = df_res[date]
        words = tokenizer.clean_text_tokenize(str(row['lead_paragraph_sw_stem']))
        for w in words:
            if w in ['covid', 'corona', 'coronaviru']:
                count = count + 1
        df_res[date] = count
    return sorted(df_res.items(), key=lambda kv: (kv[0], kv[1]))

def readPickle(pkl_file_name):
    pkl_file = open(pkl_file_name, 'rb')
    df = pickle.load(pkl_file)
    pkl_file.close()
    return df

def to_csv(pkl_file_name, csv_file_name):
    pkl_file = open(pkl_file_name, 'rb')
    df = pickle.load(pkl_file)
    pkl_file.close()
    df.to_csv(csv_file_name, index_label='index')
    
def make_wordcloud(df):
    d = {}
    for a, x in df.values:
        d[a] = x
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    wordcloud = WordCloud(background_color = "white",
                          margin = 2)
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
def create_vaccine_dict(df):
    df_res = {}
    for index, row in df.iterrows():
        date = row['date']
        if df_res.get(date) is None:
            df_res[date] = 0
        count = df_res[date]
        words = tokenizer.clean_text_tokenize(str(row['lead_paragraph_sw_stem']))
        for w in words:
            if w in ['vaccine']:
                count = count + 1
        df_res[date] = count
    return sorted(df_res.items(), key=lambda kv: (kv[0], kv[1]))

us_desks = ['National', 'U.S.']
world_desks = ['World', 'Foreign']
pkl_file_name = 'nyt.pkl'
# csv_file_name = 'nyt.csv'
df = readPickle(pkl_file_name)
# to_csv(pkl_file_name, csv_file_name)

dict_us = create_dict(df, us_desks)

total_dict = new_create_dict(df)

dict_world = create_dict(df, world_desks)
dict_monthly = create_monthly_dict(df)
dict_vaccine = create_vaccine_dict(df)



test0 = pd.DataFrame(data=total_dict)
test0.columns = ['Word','Frequency2']
test0.to_csv('Dict.csv',encoding='gbk')
make_wordcloud(test0)

#test2 = pd.DataFrame(data=dict_us)
#test2.columns = ['Word1','Frequency1']
#test2.to_csv('Dict US.csv',encoding='gbk')
#make_wordcloud(test2)

#test3 = pd.DataFrame(data=dict_world)
#test3.columns = ['Word2','Frequency2']
#test3.to_csv('Dict World.csv',encoding='gbk')
#make_wordcloud(test3)

test4 = pd.DataFrame(data=dict_monthly)
test4.to_csv('Dict Monthly.csv',encoding='gbk')
