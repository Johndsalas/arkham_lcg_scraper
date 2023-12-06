'''Script for scraping player card info from Arkhamdb websight'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

############################################ Run script #########################################

def main():
    '''Runs script'''

    # get URL's by faction
    invest, assets, events, skills = get_urls_by_type()

    # get dataframe of each card type
    skills = get_skills_df(skills)

    print("Writing to CSV...")
    # get csv of each card type  
    skills.to_csv("arkham_skills.csv")

    print("Process Complete!")

    return skills

################################# Getting URL's by card type ####################################

def get_urls_by_type():
    '''Scrapes arkhamdb and returns a list of urls pages containing card information
       on each card for each card type'''

    print("Getting investigator URL's...")
    invest = get_cata_url('investigator')

    print("Getting asset URL's...")
    assets = get_cata_url('asset')

    print("Getting event URL's...")
    events = get_cata_url('event')

    print("Getting skill URL's...")
    skills = get_cata_url('skill')

    return invest, assets, events, skills


def get_cata_url(catagory):
    ''' Child of get_urls_by_type
        Takes in a string containing a player card faction, Scrapes arkhamdb, and
        Returns a list of urls for containing information on each card of that catagory'''

    # get url for page to scrape
    url = f'https://arkhamdb.com/find?q=t%3A{catagory}&decks=player'

    # create request and soup objects
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # locate urls on page
    results = soup.find(id='list')

    results = results.find_all('a', class_='card-tip')

    # convert urls to string and make a list
    results = [str(result['href']) for result in results]

    return results

##########################Getting skill card info and creating a data frame###################

def get_skills_df(skills):
    ''' Takes in urls for skill cards and 
        Returns a df of the card info'''

    # dictionary with empty traits
    skill_traits = {'title':[],
                    'XP':[],
                    'test_icons':[],
                    'traits':[],
                    'faction':[],
                    'ability':[],
                    'type':[],
                    'flavor':[],
                    'artist':[],
                    'expansion':[]}

    print("Getting skill cards")

    # for each url get player card info from that page and add each element to skill_traits
    for url in skills:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # extract card elements
        title, xp, test_icons, traits, faction, ability, tipe, flavor, artist, expansion = get_card_traits(results)
        
        print(f'Getting Skill card {title}...')

        # list of trait values
        trait_list = [title, xp, test_icons, traits, faction, ability, tipe, flavor, artist, expansion]

        # itterate through card elements and add each to a dictionary
        for i, key in enumerate(skill_traits):

            skill_traits[key].append(trait_list[i])

    print("Making dataframe...")

    # convert dictionary to dataframe
    df_skill = pd.DataFrame(skill_traits)

    return df_skill

############################ children of get_skills_df########################################


def get_soup(url):
    '''Child of get_skills_df
       Takes in a url for a card
       Returns html request result parsed using beautiful soup'''

    # create request and soup objects
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # locate urls on page and return
    return soup.find(id='list')


def get_card_traits(results):
    ''' Child of get_skills_df
        Takes in html request result
        Returns card traits for that request'''

    # extract card elements, convert them to text, and do some initial cleaning
    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '')
    
    xp =  get_xp(results)

    test_icons = get_icons(results)

    traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    ability = get_ability(results)

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    flavor = results.find('div', class_='card-flavor small').text.replace('\n', '').replace('\t', '')

    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '')

    return title, xp, test_icons, traits, faction, ability, tipe, flavor, artist, expansion


############# Children of get_card_traits ############## 


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
        
        return xp.text.replace('\n', '').replace('\t', '')


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


def get_ability(results):
    '''Child of get_card_traits
        Takes in request results for an arkhamdb page containing player card data
        Returns a string represintation of skill test icons on the card'''
    
    # gets html object containing ability text
    ability = get_ability_html(results)
    
    # convert html to string and replace icons in text with string represintations
    ability = get_ability_string(ability)
    
    return ability


############################### Children of get_ability ############################

def get_ability_html(results):
    '''Child of get_ability
       Takes in request results for an arkhamdb page containing player card data
       Returns a string containing ability text of the card'''

    # itterate through factions to find class name for ability text and get bs object containing text
    factions = ['guardian', 'mystic', 'neutral', 'rogue', 'seeker', 'survivor']

    for faction in factions:

        ability = results.find('div', class_=f'card-text border-{faction}')
        
        # break loop if result is found
        if ability != None:

            break
            
    return ability


def get_ability_string(ability):
    '''Child of get_ability
       Takes in html object contining player card ability text
       Converts object to a string
       Replaces html indicating an icon with uppercase word equivalent
       Performs minor cleaning
       Returns a string containing the cards ability text'''
      
    # convert html to string
    ability = str(ability)
        
    # replace icon html with matching uppercase word
    icon_types = ['wild', 'willpower', 'combat', 'agility', 'intellect']
    
    for icon in icon_types:
    
        ability = ability.replace(f'<span class="icon-{icon}" title="{icon.capitalize()}"></span>', 
                                  f'{icon.upper()}')

    # delete extraneous html
    html = ['<div class="card-text border-rogue">\n<p>',
            '<div class="card-text border-survivor">\n<p>',
            '<div class="card-text border-seeker">\n<p>',
            '<div class="card-text border-guardian">\n<p>',
            '<div class="card-text border-mystic">\n<p>',
            '<div class="card-text border-neutral">\n<p>',
            '</p>\n</div>',
            '</p>',
            '<p>',
            '<b>',
            '<1>',]
    
    for item in html:
        
        ability = ability.replace(item,'')

    return ability



if __name__ == "__main__":

    main()
