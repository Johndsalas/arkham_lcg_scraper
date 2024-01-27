''' Contains code for scraping info for investigator cards'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from helper import get_soup, get_text_for_icon, clean_html

def get_invest_df(invest):

    investigator_dict = { 'title':[],
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
                            'elder_sign_ability':[],
                            'artist':[],
                            'expansion':[],
                            'flavor':[],
                            'deck_size':[],
                            'class_choices':[],
                            'secondary_class_selection':[],
                            'deckbuilding_options':[],
                            'deckbuilding_requirements':[],
                            'additional_requirements':[],
                            'additional_restrictions':[],
                            'additional_setup':[],
                            'trait_choice':[],
                            'bonus experience':[],
                            'additional_upgrade_options':[],
                            'url':[]}

    # for each url get player card info from that page and add each element to skill_traits
    for url in invest:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # get list of card elements card elements
        trait_list = get_invest_traits(results)

        trait_list.append(url)

        print(f'Getting investigator card {trait_list[0]}...')

        # itterate through card element titles and add each to a dictionary
        for i, key in enumerate(investigator_dict):

            investigator_dict[key].append(trait_list[i])

    print("Making dataframe...")

    return pd.DataFrame(investigator_dict)

def get_invest_traits(results):
    '''Scrapes website for investigator card data
       Returns a list of those values'''

    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '') + ': ' + results.find('div', class_='card-subname small').text.replace('\n', '').replace('\t', '')

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')

    willpower, intellect, combat, agility = get_stat_line(results)

    health, sanity = get_stam_line(results)
   
    ability, star = get_ability_star(results, faction)
    
    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '') 

    try:
        
        flavor = results.find_all('div', class_='card-flavor small')[1].text.replace('\n', '').replace('\t', '')

    except:
        
        flavor = ''
        
    deck_size, class_choices, secondary_class_selection, deckbuilding_options, deckbuilding_requirements, additional_requirements, additional_restrictions, additional_setup, trait_choice, bonus_experience, additional_upgrade_options = get_deck_reqs(results, faction)
    
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
            star, 
            artist,
            expansion,
            flavor,
            deck_size,
            class_choices,
            secondary_class_selection,
            deckbuilding_options,
            deckbuilding_requirements,
            additional_requirements,
            additional_restrictions,
            additional_setup,
            trait_choice,
            bonus_experience,
            additional_upgrade_options]


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


def get_ability_star(results, faction):
    '''Scrapes websight for ability text and seperates into ability and star ability'''

    ability_star =  str(results.find('div', class_=f'card-text border-{faction.lower()}'))

    ability_star = get_text_for_icon(ability_star)

    ability_star = clean_html(ability_star)

    ability_star = re.search(r'([\s\S]+?)' + f'ELDER_SIGN effect:' + r'([\s\S]+)', ability_star)

    ability = ability_star.group(1)

    star = ability_star.group(2)
    
    return ability, star

def get_deck_reqs(results,faction):
    
    deck_traits = results.find_all('div', class_=f'card-text border-{faction.lower()}')[1].text

    deck_traits = deck_traits.replace('Secondary Class Choice', 'Secondary Class Selection')

    cats = '''(Secondary Class Selection|Class Choices|Trait Choice|Deckbuilding Options|Deckbuilding Requirements|Additional Requirements|Additional Restrictions|Additional Setup|Bonus Experience|Secondary Class Choice|Additional Upgrade Options|\n)'''

    cat_list = [ 'Deck Size',
                 'Class Choices',
                 'Secondary Class Selection',
                 'Deckbuilding Options',
                 'Deckbuilding Requirements',
                 'Additional Requirements',
                 'Additional Restrictions',
                 'Additional Setup',
                 'Trait Choice',
                 'Bonus Experience',
                 'Additional Upgrade Options']

    values = []

    for cat in cat_list:

        try:

            match = re.search(f'{cat}' + r'([\s\S]+?)' + f'{cats}', deck_traits).group(1)

        except:

            match = "NONE"

        values.append(match)
    
    return values



