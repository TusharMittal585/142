import numpy as np
import csv
import pandas as pd

df=pd.read_csv('articles.csv')

C = df['vote_average'].mean()
m = df['vote_count'].quantile(0.9)
q_articles = df.copy().loc[df['vote_count'] >= m] 

def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

q_articles['score'] = q_articles.apply(weighted_rating, axis=1)

q_movies = q_articles.sort_values('score', ascending=False)
q_movies[['title', 'vote_count', 'vote_average', 'score']].head(10)