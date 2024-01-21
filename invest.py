''' Contains code for scraping info for investigator cards'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from helper import get_soup, get_text_for_icon, clean_html

def get_invest_df(invest):

    investigator_traits = { 'title':[],
                            'faction':[],
                            'type':[],
                            'traits':[],                      
                            'willpower':[],
                            'intellect':[],
                            'combat':[],
                            'agility':[],                       
                            'health':[],
                            'sanity':[],                     
                            'ability':[],
                            'artist':[],
                            'expansion':[],
                            'flavor':[],
                            'deck_size':[],
                            'deck_options':[],
                            'must_include':[],
                            'setup':[]}

    # for each url get player card info from that page and add each element to skill_traits
    for url in invest:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # get list of card elements card elements
        trait_list = get_invest_traits(results)

        print(f'Getting investigator card {trait_list[0]}...')

        # itterate through card element titles and add each to a dictionary
        for i, key in enumerate(investigator_traits):

            investigator_traits[key].append(trait_list[i])

    print("Making dataframe...")

    return pd.DataFrame(investigator_traits)

def get_invest_traits(results):
    '''Scrapes website for investigator card data
       Returns a list of those values'''

    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '')

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')

    willpower, intellect, combat, agility = get_stat_line(results)

    health, sanity = get_stam_line(results)
   
    ability = str(results.find('div', class_=f'card-text border-{faction.lower()}'))

    ability = clean_html(get_text_for_icon(ability))

    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '') 

    try:
        
        flavor = results.find_all('div', class_='card-flavor small')[1].text.replace('\n', '').replace('\t', '')

    except:
        
        flavor = ''
        
    deck_size, deck_options, must_include, setup = get_deck_reqs(results, faction)
    
    return [title, 
            faction, 
            tipe, 
            traits, 
            willpower, 
            intellect, 
            combat, 
            agility, 
            health, 
            sanity,
            ability, 
            artist,
            expansion,
            flavor,
            deck_size,
            deck_options,
            must_include,
            setup]


def get_stat_line(results):
    ''' scrapes website for investigator stat line'''

    stat_line = results.find('div', class_='card-props').text.replace('\n', '').replace('\t', '')

    stat_list = [int(char) for char in str(stat_line) if char.isnumeric() == True]

    return stat_list[0], stat_list[1], stat_list[2], stat_list[3]


def get_stam_line(results):
    ''' scrapes website for investigator health and sanity'''

    stat_line = results.find('div', class_='card-props').find_next().text.replace('\n', '').replace('\t', '')

    stat_list = [int(char) for char in str(stat_line) if char.isnumeric() == True]

    return stat_list[0], stat_list[1]


def get_deck_reqs(results, faction):

    deck = results.find_all('div', class_=f'card-text border-{faction.lower()}')[1].text

    pattern = r'(?:\b(?:Deck Size|Deckbuilding Options|Deckbuilding Requirements|Additional Setup):|\b\s*)([^:\n]+)'

    deck_split = re.findall(pattern, str(deck))

    deck_size = re.search('[0-9]{2}', deck_split[0]).group()

    deck_options = deck_split[1].replace('Deckbuilding Requirements (do not count toward deck size)', '').replace('(', '').replace(')', '').replace('  ', ' ')

    must_include = deck_split[2].replace('.Additional Setup', '')

    try:

        setup = deck_split[3]

    except:

        setup = 'NONE'

    return deck_size, deck_options, must_include, setup



