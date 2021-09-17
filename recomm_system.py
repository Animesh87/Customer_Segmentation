import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
#import warnings
#warnings.filterwarnings("ignore")
#from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import datetime as dt



rating_df = pd.read_csv("Datasets/updated_new.csv")

rating_df = rating_df[rating_df['StockCode'] != "BANK CHARGES"]
rating_df = rating_df[rating_df['StockCode'] != "DOT"]
rating_df = rating_df[rating_df['StockCode'] != "C2"]
rating_df = rating_df[rating_df['StockCode'] != "PADS"]

product_description = rating_df['Description'].drop_duplicates()

tfv =  TfidfVectorizer(min_df=3, max_features=1000, analyzer="word", 
                       stop_words="english", ngram_range = (1, 3),
                      strip_accents='unicode' , token_pattern = r'\w{1,}')

product_description = product_description.fillna(" ")

tfv_matrix = tfv.fit_transform(product_description)

sig = sigmoid_kernel(tfv_matrix,tfv_matrix)

indices = pd.Series(product_description.index,index=product_description).drop_duplicates()

def content_recomm(title,sig=sig):
    ind = indices[title]
    sig_scores = list(enumerate(sig[ind]))
    sig_scores = sorted(sig_scores, key = lambda x: x[1] , reverse=True)
    sig_scores = sig_scores[1:8]
    product_indices = [i[0] for i in sig_scores]
    return product_description.iloc[product_indices].tolist()

#print(content_recomm('WHITE HANGING HEART T-LIGHT HOLDER'))



mean_rating = pd.DataFrame(rating_df.groupby('Description')['Rating'].mean())

ratings_matrix = rating_df.pivot_table(values="Rating",index="CustomerID",columns="Description")

mean_rating['No. of ratings'] = rating_df.groupby('Description')['Rating'].count()

def CF_items(item):
    item_ratings = ratings_matrix[item]
    item_ratings_corr = ratings_matrix.corrwith(item_ratings)
    item_ratings_corrdf = pd.DataFrame(item_ratings_corr,columns=["Corrleation"]) 
    item_ratings_corrdf.dropna(inplace=True)
    item_ratings_corrdf = item_ratings_corrdf.join(mean_rating['No. of ratings'])
    item_ratings_corrdf = item_ratings_corrdf[item_ratings_corrdf['No. of ratings']>100].sort_values('Corrleation',ascending=False)
    return item_ratings_corrdf.head(5).index.tolist()

