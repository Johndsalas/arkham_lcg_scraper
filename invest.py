''' Contains code for scraping info for investigator cards'''

# Imports
import re
import pandas as pd
from helper import get_soup, get_text_for_icon, clean_html, get_clean_text

def get_invest_df(invest):
    '''Takes in urls for investigator cards and 
       Returns a df containing each cards information'''

    # dictionary with empty traits
    investigator_dict = {'title':[],
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

    print("Getting investigator cards...")

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
    '''Takes in result of html request for an investigator card
       Returns list of parsed results containing the card's information'''

    # search html request for desiered values
    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '') + ': ' + results.find('div', class_='card-subname small').text.replace('\n', '').replace('\t', '')

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '').replace('.','')

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
    '''Takes in result of html request for an investigator card
       Returns value of card's willpower, intellect, combat, agility
       as a string'''

    stat_line = results.find('div', class_='card-props').text.replace('\n', '').replace('\t', '')

    stat_list = [int(char) for char in str(stat_line) if char.isnumeric() == True]

    return stat_list[0], stat_list[1], stat_list[2], stat_list[3]


def get_stam_line(results):
    '''Takes in result of html request for an investigator card
       Returns value of card's health and stamana'''

    stat_line = results.find('div', class_='card-props').find_next().text.replace('\n', '').replace('\t', '')

    stat_list = [int(char) for char in str(stat_line) if char.isnumeric() == True]

    return stat_list[0], stat_list[1]


def get_ability_star(results, faction):
    '''Takes in result of html request for an investigator card
       Returns card's ability and star ability as strings'''

    # search results for ability texts
    ability_star =  str(results.find('div', class_=f'card-text border-{faction.lower()}'))

    # replace game icon symbles with string representantion
    ability_star = get_text_for_icon(ability_star)

    # remove htlm code from text
    ability_star = clean_html(ability_star)

    # capture each ability separately
    ability_star = re.search(r'([\s\S]+?)' + f'ELDER_SIGN effect:' + r'([\s\S]+)', ability_star)

    ability = ability_star.group(1)

    star = ability_star.group(2)
    
    return ability, star


def get_deck_reqs(results,faction):
    '''Takes in result of html request for an investigator card
       Returns card's deck construction and setup information'''
    
    # search request results for card information
    deck_traits = results.find_all('div', class_=f'card-text border-{faction.lower()}')[1].text

    # replace text to avoid scraping difficulties
    deck_traits = deck_traits.replace('Secondary Class Choice', 'Secondary Class Selection')

    cat_list = ['Deck Size',
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

    stop_capture = '(Secondary Class Selection|Class Choices|Trait Choice|Deckbuilding Options|Deckbuilding Requirements|Additional Requirements|Additional Restrictions|Additional Setup|Bonus Experience|Secondary Class Choice|Additional Upgrade Options|\n)'

    # itterate through catagories in cat_list capture from apearance catagory in text untill another catagory name is encountered
    # add captured text to values list
    # if catagory not found add 'NONE'
    for cat in cat_list:

        try:

            match = get_clean_text(re.search(f'{cat}' + r'([\s\S]+?)' + f'{stop_capture}', deck_traits).group(1))

        except:

            match = "NONE"

        values.append(match.replace('(do not count toward deck size)', '').replace('( and/or )',''))

        stop_capture = stop_capture.replace(f'{cat}|','')
    
    return values



