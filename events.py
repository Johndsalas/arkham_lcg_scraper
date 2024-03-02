''' Contains code for scraping info for event cards'''

# Imports
import pandas as pd
from helper import get_soup, get_cost_xp, get_subtitle, get_traits, get_ability, get_clean_text, get_icons


def get_events_df(event_urls):
    ''' Takes in urls for event cards and 
        Returns a df containing each cards information'''

    # dictionary with empty traits
    event_dict = {'title':[],
                  'sub_title':[],
                  'faction':[],
                  'type':[],
                  'traits':[],
                  'cost':[],
                  'XP':[],
                  'test_icons':[],
                  'ability':[],
                  'artist':[], 
                  'expansion':[],
                  'flavor':[],
                  'url':[]}

    print("Getting event cards...")

    # for each url get player card info from that page and add each element to event_traits
    for url in event_urls:

        # make html request to arkham db and parse using BS
        results = get_soup(url)

        # extract card elements
        event_list = get_event_traits(results)
        
        event_list.append(url)

        print(f'Getting event card {event_list[0]}...')

        # itterate through card elements and add each to a dictionary
        for i, key in enumerate(event_dict):

            event_dict[key].append(event_list[i])

    print("Making dataframe...")

    # convert dictionary to dataframe
    df_event = pd.DataFrame(event_dict)

    return df_event


def get_event_traits(results):
    '''Takes in result of html request for an event card
       Returns list of parsed results containing the card's information'''

    # search html request for desiered values
    title = results.find('a', class_='card-name card-tip').text.replace('\n', '').replace('\t', '').replace('"','')

    sub_title = get_subtitle(results)

    faction = results.find('span', class_='card-faction').text.replace('\n', '').replace('\t', '')

    tipe = results.find('span', class_='card-type').text.replace('\n', '').replace('\t', '')

    traits = get_clean_text(get_traits(results))

    cost, xp = get_cost_xp(results)

    icons = get_icons(results)

    ability = get_ability(results, faction)

    artist = results.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    flavor = results.find('div', class_='card-flavor small').text.replace('\n', '').replace('\t', '').replace('"','')

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
             flavor]