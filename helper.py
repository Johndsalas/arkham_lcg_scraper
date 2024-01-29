''' Contains helper functions for invest.py, skills.py, accesseries.py, and events.py'''

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url):
    '''Takes in a url for a card
       Returns html request result parsed using beautiful soup'''

    # create request and soup objects
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # locate urls on page and return
    return soup

def get_text_for_icon(text):

    # replace icon html with matching word in all caps
    icon_types = [
                  'action',
                  'reaction',
                  'wild', 
                  'willpower', 
                  'combat', 
                  'agility', 
                  'intellect', 
                  'wild',
                  'curse', 
                  'bless',
                  'rogue',
                  'survivor',
                  'seeker',
                  'guardian',
                  'mystic',
                  'neutral',
                  'skull',
                  'tablet',
                  'cultist',
                  'elder sign']
    
    for icon in icon_types:
    
        text = text.replace(f'<span class="icon-{icon}" title="{icon.capitalize()}"></span>', 
                                  f'{icon.upper()}')
        
        text = text.replace(f'<div class="card-text border-{icon}">\n<p>', '')

    text = text.replace(f'<span class="icon-wild" title="Any Skill"></span>', 'WILD')

    text = text.replace(f'<span class="icon-elder_sign" title="Elder Sign"></span>', 'ELDER_SIGN')

    text = text.replace(f'<span class="icon-elder_sign" title="Elder Thing"></span>', 'ELDER_THING')

    text = text.replace(f'<span class="icon-lightning" title="Fast Action"></span>', 'FAST ACTION')

    text = text.replace(f'<span class="icon-auto_fail" title="Auto Fail"></span>', 'TENTACLES')

    return text

def clean_html(text):

    # delete extraneous html
    dirt = [
            '</p>\n</div>',
            '</p>',
            '<p>',
            '<b>',
            '</b>',
            '<br/',
            '<1>',
            '<i>',
            '</i>',
            '><span>']
    
    for item in dirt:
        
        text = text.replace(item,'')

    return text