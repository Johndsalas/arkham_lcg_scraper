''' Contains code for scraping info for investigator cards'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


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
                            'must_include':[]}

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


def get_soup(url):
    '''Takes in a url for a card
       Returns html request result parsed using beautiful soup'''

    # create request and soup objects
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # locate urls on page and return
    return soup.find(id='list')


def get_invest_traits(results):
    '''Scrapes website for investigator card data
       Returns a list of those values'''

    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '')

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')

    willpower, intellect, combat, agility = get_stat_line(results)

    health, sanity = get_stam_line(results)
   
    ability = clean_ability_string(results, faction)

    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '') 

    try:
        
        flavor = results.find_all('div', class_='card-flavor small')[1].text.replace('\n', '').replace('\t', '')

    except:
        
        flavor = ''
        
    deck_size, deck_options, must_include = get_deck_reqs(results, faction)
    
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
            must_include]


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
    ''' scrapes website for investigator deckbuilding requirements'''

    deck = results.find_all('div', class_=f'card-text border-{faction.lower()}')[1].text

    deck_split = re.split(':', deck)

    deck_size = re.search('[0-9]{2}', deck_split[1]).group()
    
    deck_options = re.search('^(.*?\.)', deck_split[2]).group()[1:-1].replace('(', '').replace(')', '').replace('  ', ' ')

    must_include = re.search('^(.*?\.)', deck_split[3]).group()[1:-1].replace('(', '').replace(')', '').replace('  ', ' ')
    
    return deck_size, deck_options, must_include


def clean_ability_string(results, faction):
    
    ability = str(results.find('div', class_=f'card-text border-{faction.lower()}'))

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
    
        ability = ability.replace(f'<span class="icon-{icon}" title="{icon.capitalize()}"></span>', 
                                  f'{icon.upper()}')
        
        ability = ability.replace(f'<div class="card-text border-{icon}">\n<p>', '')

    ability = ability.replace(f'<span class="icon-wild" title="Any Skill"></span>', 'WILD')

    ability = ability.replace(f'<span class="icon-elder_sign" title="Elder Sign"></span>', 'ELDER_SIGN')

    ability = ability.replace(f'<span class="icon-elder_sign" title="Elder Thing"></span>', 'ELDER_THING')

    ability = ability.replace(f'<span class="icon-lightning" title="Fast Action"></span>', 'FAST ACTION')

    ability = ability.replace(f'<span class="icon-auto_fail" title="Auto Fail"></span>', 'TENTACLES')
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
            '><span>',]
    
    for item in dirt:
        
        ability = ability.replace(item,'')

    return ability
