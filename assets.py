''' Contains code for scraping asset cards'''

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from helper import get_soup, get_clean_text, get_cost_xp, get_subtitle, get_traits, get_ability, get_icons

def get_assets_df(asset_urls):
    ''' Takes in urls for asset cards and 
        Returns a df containing each cards information'''

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
                  'slot':[],
                  'url':[]}

    # gathers list of URL's belonging to each 'slot' catagory (information is otherwise unavailable)
    one_hand = get_slot_url('https://arkhamdb.com/find?q=z%3Ahand&decks=player')

    two_hand = get_slot_url('https://arkhamdb.com/find?q=z%3A%22hand+x2%22&decks=player')

    accessory = get_slot_url('https://arkhamdb.com/find?q=z%3Aaccessory&decks=player')

    ally = get_slot_url('https://arkhamdb.com/find?q=z%3Aally&decks=player')

    one_arcane = get_slot_url('https://arkhamdb.com/find?q=z%3Aarcane&decks=player')

    two_arcane = ['https://arkhamdb.com/card/06328']

    print("Getting asset cards...")

    # for each url get player card info from that page and add each element to event_traits
    for url in asset_urls:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # extract card elements
        asset_list = get_asset_traits(results)
        
        asset_list.append(get_item_slot(one_hand, two_hand, accessory, ally, one_arcane, two_arcane, url))
        
        asset_list.append(url)

        print(f'Getting asset card {asset_list[0]}...')

        # itterate through card elements and add each to a dictionary
        for i, key in enumerate(asset_dict):

            asset_dict[key].append(asset_list[i])

    print("Making dataframe...")

    # convert dictionary to dataframe
    df_asset = pd.DataFrame(asset_dict)

    return df_asset


def get_asset_traits(results):
    '''Takes in result of html request for an asset card
       Returns list of parsed results containing the card's information'''
    
    # search html request for desiered values
    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '').replace('"','')

    sub_title = get_subtitle(results)

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = get_clean_text(results.find('span', class_='card-type').text.replace('\n', '').replace('\t', ''))

    traits = get_clean_text(get_traits(results))

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


def get_asset_stam_line(results):
    '''Takes in request results for an arkhamdb page containing player card data
        Returns two strings containing health and sanity values for that card'''
    
    # look for and return health and sanity values if not found return '--'
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


def get_slot_url(scrape_url):
    '''Takes in a url to a page of search results containing cards of one slot type
       Returns list of urls from that page'''
    
    # make request
    html = requests.get(scrape_url)

    soup = BeautifulSoup(html.content, 'html.parser')

    # locate urls on page
    results = soup.find(id='list')

    results = results.find_all('a', class_='card-tip')

    # convert urls to string and make a list
    urls = [str(result['href']) for result in results]

    return urls


def get_item_slot(one_hand, two_hand, accessory, ally, one_arcane, two_arcane, url):
    '''Takes in a list of url's and one url to be checked 
       Returns a string containing the slot value of the coresponding card '''

    # check lists for url and return the corresponding slot if not founf return '--'
    if url in one_hand:
    
        return 'One Handed'
    
    elif url in two_hand:
        
        return 'Two Handed'
        
    elif url in accessory:

        return 'Accessory'
        
    elif url in ally:
        
        return 'Ally'
        
    elif url in one_arcane:
        
        return 'One Arcane'
        
    elif url in two_arcane:
        
        return 'Two Arcane'
    
    else:

        return '--'