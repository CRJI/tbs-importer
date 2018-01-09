# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import sys
from sqlalchemy import create_engine

from utils import readers, transformers, writers

model = sys.argv[1]
if len(sys.argv) > 2:
    output_file = sys.argv[2]
else:
    output_file = '{}.json'.format(model)

db_user = 'root'
db_pass = 'secret'
db_host = '127.0.0.1'
db_name = 'theblack_production'

dsn = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
    db_user,
    db_pass,
    db_host,
    db_name,
)

db = create_engine(
    dsn,
    encoding='utf-8',
    convert_unicode=False
)

db.execute('SET NAMES utf8mb4')
db.execute('SET CHARACTER SET utf8mb4')
db.execute('SET character_set_connection=utf8mb4')


def get_reader(model):
    return {
        'authors': readers.AuthorsReader(db),
        'stories': readers.StoriesReader(db),
        'stories_pages': readers.StoriesReader(db),
        'blogs': readers.BlogsReader(db),
        'dossiers': readers.DossiersReader(db),
    }[model]

def get_writer(model, item):
    return {
        'authors': writers.BaseWriter(item),
        'stories': writers.BaseWriter(item),
        'stories_pages': writers.BaseWriter(item),
        'blogs': writers.BaseWriter(item),
        'dossiers': writers.BaseWriter(item),
    }[model]

def get_transformer(model, item):
    return {
        'authors': transformers.AuthorsTransformer(item),
        'stories': transformers.StoriesTransformer(item),
        'stories_pages': transformers.StoriesPagesTransformer(item),
        'blogs': transformers.BlogsTransformer(item),
        'dossiers': transformers.DossiersTransformer(item),
    }[model]

with open(output_file, 'w') as outfile:
    last_idx = get_reader(model).read().iloc[-1].name
    outfile.write('[\n')
    for index, item in get_reader(model).read().iterrows():
        transformed = get_transformer(model, item)
        transformed = transformed.transform()
        writer = get_writer(model, transformed)
        outfile.write(writer.dump())
        if last_idx != index:
            outfile.write(',')
        outfile.write('\n')
    outfile.write(']')
