# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import dateparser
import re
import ipdb


class StoriesScraper:

    def __init__(self):
        self.baseUrl = 'https://theblacksea.eu'
        self.urls = [
            "/malta-files/article/en/cash-loans-czar-maltese-tax-escape-plan",
            "/malta-files/article/en/erdogan-family-secret-offshore-ship-deal",
            "/malta-files/article/en/erdogan-offshore-bank-account",
            "/malta-files/article/en/erdogan-offshore-update",
            "/malta-files/article/en/erdogans-son-in-law-off-shore-tax-scheme",
            "/malta-files/article/en/family-business-turkey-prime-minister-offshore",
            "/malta-files/article/en/socar-tanker-purchase-erdogan-family",
            "/malta-files/article/en/turkish-pm-family-secret-offshore-mosque",
            "/malta-files/article/tr/bir-degil-uc-erdogan-offshore-guncelleme",
            "/malta-files/article/tr/calik-holding-offshore-plani-albayrak",
            "/malta-files/article/tr/erdogan-ailesinin-gizlice-socar-a-satilan-gemileri",
            "/malta-files/article/tr/erdogan-ailesinin-gizli-offshore-anlasmasmi",
            "/malta-files/article/tr/erdogan-offshore-banka-hesabi",
            "/malta-files/article/tr/yildirim-ailesinin-yeni-gemileri-ve-offshore-serveti",
            "/stories/article/en/court-secrets-ocampo-explainer",
            "/stories/article/en/erdogan-and-the-kurds",
            "/stories/article/en/exorcism-romanian-style",
            "/stories/article/en/gucci-tax",
            "/stories/article/en/icc-ocampo-bensouda-fallout",
            "/stories/article/en/icc-ocampo-clooney-jolie",
            "/stories/article/en/icc-ocampo-kenya",
            "/stories/article/en/icc-yezidi-lobby-scandal",
            "/stories/article/en/italy_neofascist_business_crimea",
            "/stories/article/en/living-on-the-edge-photostory",
            "/stories/article/en/messi-tax",
            "/stories/article/en/mothers-leave-romania",
            "/stories/article/en/romania-worker-sell-out",
            "/stories/article/en/second-to-last-serbia-migrants",
            "/stories/article/en/the-mafia-ambassador",
            "/stories/article/en/uzbekistan-lola-karimova-business",
            "/stories/article/en/volkswagen-luxembourg-tax",
            "/stories/article/ro/exorcism-romanian-style",
            "/stories/article/tr/erdogan-and-the-kurds",
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

        details = {
            'seo_title': bs.title.string,
            'title': main_info.h1.span.string,
            'intro': main_info.h2.span.string if main_info.h2 else main_info.h1.span.string,
            'authors': '1',
            'date': dateparser.parse(main_info.h4.span.string, languages=['en', 'tr', 'ro']),
            'content': content,
            'pk': pk
        }

        print("[{}] {}".format(
            details['date'],
            url
        ))

        return details
