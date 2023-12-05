'''Script for scraping player card info from Arkhamdb websight'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


#################################Getting URL's by card type####################################

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

    # for each url get player card info from that page and add each element to skill_traits
    for url in skills:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # extract card elements
        title, xp, test_icons, traits, faction, ability, tipe, flavor, artist, expansion = get_card_traits(results)
        
        # list of trait values
        trait_list = [title, xp, test_icons, traits, faction, ability, tipe, flavor, artist, expansion]

        # itterate through card elements and add each to a dictionary
        for i, key in enumerate(skill_traits):

            skill_traits[key].append(trait_list[i])

    # convert dictionary to dataframe
    df_skill = pd.DataFrame(skill_traits)

    return df_skill


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
    
        # use 
        title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '')
        
        xp =  get_xp(results)

        test_icons = get_icons(results)

        traits = results.find('p', class_='card-traits').text.replace('\n', '').replace('\t', '')

        faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

        ability = get_ability_text(results)

        tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

        flavor = results.find('div', class_='card-flavor small').text.replace('\n', '').replace('\t', '')

        artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

        expansion = results.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '')

        return title, xp, test_icons, traits, faction, ability, tipe, flavor, artist, expansion