''' Contains code for scraping info for investigator cards'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def get_invest_df(invest_urls):

    invest_traits{
                               'title':[],
                           'traits':[],
                           'faction':[],  
                           'willpower':[],
                           'intellect':[],
                           'combat':[],
                           'agility':[],
                           'health':[],
                           'sanity':[],
                           'ability':[],
                           'deck_size':[],
                           'deckbuilding':[],
                           'intro':[],
                           'type':[],
                           'flavor':[],
                           'artist':[],
                           'expansion':[]