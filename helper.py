''' Contains helper functions for invest.py, skills.py, accesseries.py, and events.py'''

import requests
import re
from bs4 import BeautifulSoup


def get_soup(url):
    '''Takes in a url for a card
       Returns html request result parsed using beautiful soup'''

    # create request and soup objects
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # locate urls on page and return
    return soup

def get_text_for_icon(text):
    '''Takes in request response as a string
       replaces html code indicating a game icon with a text representation
       Returns sting with replacements'''
    
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
    '''Takes in request response as a string
       Removes common unwanted html patters from string
       Returns string with patterns removed'''
    
    # remove each item in dirt from text
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
    '''Takes in request response as a string
       Returns subtitle as string or '--' if not found'''
    
    try:
        
        sub_title = results.find('div', class_='card-subname small').text.replace('\n', '').replace('\t', '')
        
    except:
        
        sub_title = '--'
        
    return sub_title



def get_traits(results):
    '''Takes in request response as a string
       Returns traits value as string or '--' if not found'''
    
    try:
        
        traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')
        
    except:
        
        traits = '--'
        
    return traits


def get_cost_xp(results):
    '''Takes in request response as a string
       Returns cost and XP values as string or '--' if not found'''

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
    '''Takes in request results for an arkhamdb page containing player card data
        Returns a string containing ability text for that card'''
    
    # gets html object and convert to string
    ability_string = str(results.find('div', class_=f'card-text border-{faction.lower()}'))
    
    # convert html to string, replace icons in text with string represintations
    ability_text = get_text_for_icon(ability_string)

    ability_text = clean_html(ability_text)
    
    return ability_text


def get_clean_text(text):
    '''Takes in request response as a string
       Removes common unwanted text patters from string
       Returns string with patterns removed'''

    dirt = ['.',
            ':',
            '()',
            '(, , , , or )',
            '(, , , , and )']

    for item in dirt:

        text = text.replace(item, '')

    return text


def get_icons(results):
    '''Takes in request results for an arkhamdb page containing player card data
        Returns a string represintation of test icons on the card'''
      
    icons = ''

    # list containing each icon type
    icon_types = ['wild', 'willpower', 'combat', 'agility', 'intellect']

    # itterate through icon types
    for stat in icon_types:

        # get number of that icon on card from request results
        num_icons = len(results.find_all('span', class_=f'icon icon-{stat} color-{stat}'))

        # add that icon name to a string for each time it appears in request results
        for icon in range(num_icons):

            icons += f'{stat} '
            
    return icons.upper()[:-1]