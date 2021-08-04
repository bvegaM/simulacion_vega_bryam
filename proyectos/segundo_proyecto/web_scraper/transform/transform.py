import argparse
import coloredlogs
import hashlib
from langdetect import detect
import logging
logging.basicConfig(level=logging.INFO)
import nltk
import pandas as pd
import re
import uuid

from nltk.corpus import stopwords
from urllib.parse import urlparse


stop_words = set(stopwords.words('english'))
logger = logging.getLogger(__name__)
coloredlogs.install()

def main(filename):
    logger.info('Starting cleaning process')
    df = pd.read_csv('../data/{}'.format(filename))
    df = generate_uuid(df,'abstract')
    df = obtain_columns(df,['uuid','abstract'])
    df = remove_new_lines_from_abstract(df)
    df = split_words(df,'abstract',int(input('limit words in abstract: ')))
    df = tokenize_column(df,'abstract')
    df = get_tokens(df,'abstract')
    df = get_language(df,'abstract')
    df = df[df['language']=='en']
    df = df.drop(['split'],axis=1)
    save_data(df,filename)

def generate_uuid(df,column_name):
    logger.info('Generating uuid')
    
    df['uuid'] = df[column_name].apply(lambda x: uuid.uuid4().hex)
    return df

def obtain_columns(df,columns):
    logger.info('Get principal columns')

    return df[columns]

def remove_new_lines_from_abstract(df):
    logger.info('Remove new lines from abstract')

    df['abstract']=(df.apply(lambda row: row['abstract'], axis=1)
                        .apply(lambda body: re.sub(r'(\n|\r)+',r'',body)))
    return df

def split_words(df,column_name,limit):
    logger.info('Split words for {}'.format(column_name))
    
    df['split'] = df[column_name].apply(lambda x: len(x.split(' ')))
    df = df[df['split']>limit]
    return df

def tokenize_column(df,column_name):
    logger.info('Counting token words for {}'.format(column_name))

    df['n_tokens_{}'.format(column_name)] = (df.dropna().apply(lambda row:nltk.wordpunct_tokenize(row[column_name]),axis=1)
    .apply(lambda tokens: list(filter(lambda token:token.isalpha(),tokens)))
    .apply(lambda tokens: list(map(lambda token: token.lower(),tokens)))
    .apply(lambda word_list: list(filter(lambda word: word not in stop_words,word_list)))
    .apply(lambda valid_word_list: len(valid_word_list)))

    return df

def get_tokens(df,column_name):
    logger.info('Counting token words for {}'.format(column_name))

    df['tokens_{}'.format(column_name)] = (df.dropna().apply(lambda row:nltk.wordpunct_tokenize(row['abstract']),axis=1)
    .apply(lambda tokens: list(filter(lambda token:token.isalpha(),tokens)))
    .apply(lambda tokens: list(map(lambda token: token.lower(),tokens)))
    .apply(lambda word_list: list(filter(lambda word: word not in stop_words,word_list))))

    return df

def get_language(df,column_name):
    logger.info('Getting Language from {}'.format(column_name))

    df['language'] = df[column_name].apply(lambda x:detect(x))
    return df

def save_data(df,filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info('Saving data at location: {}'.format(clean_filename))

    df.to_csv(clean_filename,index=False)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)
    
    arg = parser.parse_args()

    main(arg.filename)
    
    
