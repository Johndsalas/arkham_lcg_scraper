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
            '><span>',
            '</div>',
            '<div class="card-text border-neutral>',
            '<div class="card-text border-survivor>',
            '<div class="card-text border-guardian>',
            '<div class="card-text border-mystic>',
            '<div class="card-text border-rouge>',
            '<div class="card-text border-seeker>']
    
    for item in dirt:
        
        text = text.replace(item,'')

    return text


def get_subtitle(results):
    
    try:
        
        sub_title = results.find('div', class_='card-subname small').text.replace('\n', '').replace('\t', '')
        
    except:
        
        sub_title = ''
        
    return sub_title



def get_traits(results):
    
    try:
        
        traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')
        
    except:
        
        traits = ''
        
    return traits


def get_cost_xp(results):
    
    cost_xp = str(results.find('div', class_='card-props'))

    try:
    
        cost = re.search(r'Cost:\s+(\d+)', cost_xp).group(1)
        
    except:
        
        cost = 0

    try:
    
        xp = re.search(r'XP:\s+(\d+)', cost_xp).group(1)
        
    except:
        
        xp = 0
    
    return cost, xp


def get_ability(results, faction):
    '''Child of get_card_traits
        Takes in request results for an arkhamdb page containing player card data
        Returns a string represintation of skill test icons on the card'''
    
    # gets html object and convert to string
    ability_string = str(results.find('div', class_=f'card-text border-{faction.lower()}'))
    
    # convert html to string, replace icons in text with string represintations
    ability_text = get_text_for_icon(ability_string)

    ability_text = clean_html(ability_text)
    
    return ability_text


def get_clean_text(text):

    dirt = ['.',
            ':',
            '()',
            '(, , , , or )',
            '(, , , , and )']

    for item in dirt:

        text = text.replace(item, '')

    return text