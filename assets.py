''' Contains code for scraping asset cards'''

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from helper import get_soup, get_text_for_icon, clean_html, get_cost_xp, get_subtitle, get_traits, get_ability

def get_assets_df(asset_urls):
    ''' 
        Takes in urls for event cards and 
        Returns a df of the card info
                                        '''

    # dictionary with empty traits
    asset_dict = {'title':[],
                  'sub_title':[],
                  'faction':[],
                  'type':[],
                  'traits':[],
                  'cost':[],
                  'XP':[],
                  'test_icons':[],
                  'ability':[],
                  'health':[],
                  'sanity':[], 
                  'artist':[],
                  'expansion':[],
                  'flavor':[],
                  'url':[]}


    print("Getting asset cards...")

    # for each url get player card info from that page and add each element to event_traits
    for url in asset_urls:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # extract card elements
        asset_list = get_asset_traits(results)
        
        asset_list.append(url)

        print(f'Getting event card {asset_list[0]}...')

        # itterate through card elements and add each to a dictionary
        for i, key in enumerate(asset_dict):

            asset_dict[key].append(asset_list[i])

    print("Making dataframe...")

    # convert dictionary to dataframe
    df_asset = pd.DataFrame(asset_dict)

    return df_asset

##########################################Get soup request#########################################################


def get_asset_traits(results):
    
    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '')

    sub_title = get_subtitle(results)

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = get_traits(results)

    cost, xp = get_cost_xp(results)

    icons = get_icons(results)

    ability = get_ability(results, faction)

    health, sanity = get_asset_stam_line(results)

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
             health,
             sanity,
             artist,
             expansion,
             flavor]


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


def get_asset_stam_line(results):
    
    results = results.find('div').text.replace('\n', '').replace('\t', '') 
    
    try:
    
        health = re.search(r'Health:\s+(\d+)', results).group(1)

    except:

        health = "--"
    
    try:

        sanity = re.search(r'Sanity:\s+(\d+)', results).group(1)
        
    except:

        sanity = "--"

    return health, sanity