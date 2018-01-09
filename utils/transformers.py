# -*- coding: utf-8 -*-

# from yaml import load, dump

import html
import json
import uuid
from htmllaundry import strip_markup
from slugify import slugify


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

        body = '[{"type": "aligned_html", "value": {"html": %s, "alignment": "normal"}, "id": "%s"}]'

        a['fields']['date'] = a['fields']['date'].isoformat()
        a['fields']['content'] = a['fields']['content'].replace('\r', '').replace('\n', '')
        a['fields']['body'] = body % (json.dumps(a['fields']['content']), uuid.uuid4()),
        a['fields']['body'] = a['fields']['body'][0].replace('\\\\', '\\')
        a['pk'] = a['fields']['pk']
        a['fields'].pop('pk')
        a['fields'].pop('content')
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


class StoriesPagesTransformer(BaseTransformer):

    def restructure(self):
        page = {}
        a = self.transformable.to_dict()
        page['pk'] = a['pk']
        page['model'] = 'wagtailcore.page'
        page['fields'] = {
            "title": a['title'],
            "slug": slugify(a['title']),
            "url_path": "/index/stories/{}/".format(slugify(a['title'])),
            "live": True,
            "seo_title": a['title'],
            "depth": 4,
            "content_type_id": 34,
            "path": "000100020002000{}".format(page['pk']),
        }
        self.transformable = page

    def transform(self):
        self.restructure()
        return self.transformable


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
