''' Contains code for scraping info for skill cards'''

# Imports
import re
import pandas as pd
from helper import get_soup, get_text_for_icon, clean_html, get_ability, get_clean_text, get_icons


def get_skills_df(skill_urls):
    '''Takes in urls for skills cards and 
       Returns a df containing each cards information'''

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

    print("Getting skill cards...")

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


def get_skill_traits(results):
    '''Takes in result of html request for an skills card
       Returns list of parsed results containing the card's information'''

    # search request result for desiered values
    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '').replace('"','')
    
    xp =  get_xp(results)

    test_icons = get_icons(results)

    traits = get_clean_text(results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', ''))

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    ability = get_ability(results, faction)

    tipe = get_clean_text(results.find('span', class_='card-type').text.replace('\n', '').replace('\t', ''))

    flavor = results.find('div', class_='card-flavor small').text.replace('\n', '').replace('\t', '')
    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '')

    return [title, 
            xp, 
            test_icons, 
            traits, 
            faction, 
            ability, 
            tipe, 
            flavor, 
            artist, 
            expansion]


def get_xp(results):
    '''Takes in result of html request for an skills card
       Returns XP value of that card'''
    
    # search request result for xp value an return that value or 0 if value ids not found
    xp = results.find('div', class_='card-props')
    
    if xp == None:
        
        return 0
    
    else:
        
        return re.search('[0-9]', str(xp)).group()


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


