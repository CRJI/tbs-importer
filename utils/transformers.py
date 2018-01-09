# -*- coding: utf-8 -*-

# from yaml import load, dump

import html
from htmllaundry import strip_markup

class DjangoFixtureWriter:

    def load_freezefile(fp):
        return

    def dump_fixture(fp):
        return

class BaseTransformer():

    def __init__(self, transformable):
        self.transformable = transformable

    def transform(self):
        self.restructure()
        return self.transformable

class ArticlesTransformer(BaseTransformer):

    def cleanup(self):
        a = self.transformable
        a['title'] = html.unescape(
            a['title']
        ).replace('\'\'', '\'')
        a['intro'] = strip_markup(
            html.unescape(a['intro'])
        )
        a['authors'] = a['authors'].split(',')
        for idx in a['authors']:
            # a['authors'][idx] = int(a['authors'][idx])
            idx = int(idx)
        try:
            a['dossier'] = int(float(a['dossier']))
        except:
            a['dossier'] = None
        return a

    def transform(self):
        self.cleanup()
        self.restructure()
        return self.transformable


class StoriesTransformer(ArticlesTransformer):

    def restructure(self):
        a = {}
        a['fields'] = self.transformable.to_dict()
        a['fields']['date'] = a['fields']['date'].isoformat()
        a['pk'] = a['fields']['pk']
        a['fields'].pop('pk')
        a['model'] = 'blacktail.Story'
        self.transformable = a

class BlogsTransformer(ArticlesTransformer):

    def restructure(self):
        a = {}
        a['fields'] = self.transformable.to_dict()
        a['fields']['date'] = a['fields']['date'].isoformat()
        a['pk'] = a['fields']['pk']
        a['fields'].pop('pk')
        a['fields'].pop('dossier')
        a['model'] = 'blacktail.BlogPost'
        self.transformable = a


class AuthorsTransformer(BaseTransformer):

    def restructure(self):
        a = {}
        a['fields'] = self.transformable.to_dict()
        a['pk'] = a['fields']['pk']
        a['fields'].pop('pk')
        a['model'] = 'blacktail.Author'
        self.transformable = a

    def transform(self):
        self.restructure()
        return self.transformable


class DossiersTransformer(BaseTransformer):

    def __init__(self, transformable):
        self.transformable = transformable

    def restructure(self):
        a = {}
        a['fields'] = self.transformable.to_dict()
        a['pk'] = a['fields']['pk']
        a['fields'].pop('pk')
        a['model'] = 'blacktail.StoryDossier'
        self.transformable = a
