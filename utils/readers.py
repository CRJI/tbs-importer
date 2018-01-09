# -*- coding: utf-8 -*-

import pandas as pd
from .queries import *


class AuthorsReader:

    def __init__(self, db):
        self.db = db
        # self.db_rows = self.read()

    def read(self):
        users = pd.read_sql_query(
            authors_query,
            self.db
        )
        return users

class DossiersReader:

    def __init__(self, db):
        self.db = db

    def read(self):
        dossiers = pd.read_sql_query(
            dossiers_query,
            self.db
        )
        return dossiers

class StoriesReader:

    def __init__(self, db):
        self.db = db

    def read(self):
        stories = pd.read_sql_query(
            stories_query,
            self.db
        )
        return stories

class BlogsReader:

    def __init__(self, db):
        self.db = db

    def read(self):
        blogs = pd.read_sql_query(
            blogs_query,
            self.db
        )
        return blogs
