''' Contains code for scraping info for skill cards'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from helper import get_soup, get_text_for_icon, clean_html



def get_skills_df(skill_urls):
    ''' 
        Takes in urls for skill cards and 
        Returns a df of the card info
                                        '''

    # dictionary with empty traits
    skill_dict = {'title':[],
                    'XP':[],
                    'test_icons':[],
                    'traits':[],
                    'faction':[],
                    'ability':[],
                    'type':[],
                    'flavor':[],
                    'artist':[],
                    'expansion':[],
                    'url':[]}

    print("Getting skill cards")

    # for each url get player card info from that page and add each element to skill_traits
    for url in skill_urls:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # extract card elements
        skill_list = get_skill_traits(results)
        
        skill_list.append(url)

        print(f'Getting Skill card {skill_list[0]}...')

        # itterate through card elements and add each to a dictionary
        for i, key in enumerate(skill_dict):

            skill_dict[key].append(skill_list[i])

    print("Making dataframe...")

    # convert dictionary to dataframe
    df_skill = pd.DataFrame(skill_dict)

    return df_skill

##########################################Get soup request#########################################################


def get_event_traits(results):

    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '')

    sub_title = get_subtitle(results)

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = get_traits(results)

    cost, xp = get_cost_xp(results)

    icons = get_icons(results)

    ability = get_ability(results, faction)

    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    flavor = results.find('div', class_='card-flavor small').text.replace('\n', '').replace('\t', '')

    expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '')

    return [title,
             sub_title,
             faction,
             tipe,
             traits,
             cost,
             xp,
             icons,
             ability,
             artist,
             expansion,
             flavor,
             url]


def get_xp(results):
    ''' Child of get_card_traits
        Takes in an BS object containing card information
        Returns XP cost of card if it exists
        Otherwise returns 0'''
    
    # locate xp info in object
    xp = results.find('div', class_='card-props')
    
    # if there is no value return 0
    if xp == None:
        
        return 0
    
    # otherwise return perform minor cleaning on value and return
    else:
        
        return re.search('[0-9]', str(xp)).group()


def get_icons(results):
    '''Child of get_card_traits
       Takes in request results for an arkhamdb page containing player card data
       Returns a string represintation of skill test icons on the card'''
      
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
