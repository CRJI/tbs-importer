# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parser
import re


class StoriesScraper:

    def __init__(self):
        self.baseUrl = 'https://theblacksea.eu'
        self.urls = [
            '/malta-files/article/en/cash-loans-czar-maltese-tax-escape-plan',
            '/malta-files/article/en/erdogans-son-in-law-off-shore-tax-scheme',
            '/malta-files/article/en/family-business-turkey-prime-minister-offshore',
            '/malta-files/article/en/socar-tanker-purchase-erdogan-family',
            '/malta-files/article/en/erdogan-family-secret-offshore-ship-deal',
            '/malta-files/article/en/turkish-pm-family-secret-offshore-mosque',
            '/malta-files/article/en/erdogan-offshore-update',
            '/malta-files/article/en/erdogan-offshore-bank-account',
        ]
        self.pk = 2000

    def read(self):
        stories = []
        for link in self.urls:
            self.pk += 1
            stories.append(
                self.scrape_story(
                    '{}{}'.format(self.baseUrl, link),
                    self.pk
                )
            )

        return pd.DataFrame(stories)


    def scrape_story(self, url, pk):
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'html.parser')

        main_info = bs.find('div', 'main-info')
        content_sections = bs.find_all('section', re.compile("^content-"))
        content = ''

        for section in content_sections:
            content += section.prettify()

        try:
            footer = bs.find_all('footer')[0]
            content += footer.prettify()
        except:
            pass


        return {
            'seo_title': bs.title.string,
            'title': main_info.h1.span.string,
            'intro': main_info.h2.span.string,
            'authors': '1',
            'date': date_parser(main_info.h4.span.string),
            'content': content,
            'pk': pk
        }
