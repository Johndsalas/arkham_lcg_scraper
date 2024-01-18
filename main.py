'''Script for scraping player card info from Arkhamdb websight'''

# Imports

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

from invest import get_invest_df
#from assets import get_assets_df
#from events import get_events_df
#from skills import get_skills_df

############################################ Run script #########################################

def main():
    '''Scrapes Arkhamdb websight 
       Returns a dataframe containing player card information for each card type
       Investigators, Assets, Events, and Skills'''

    # get URL's by faction
    invest, assets, events, skills = get_urls_by_type()

    # get dataframe of each card type
    invest_df = get_invest_df(invest)
    # assets_df = get_assets_df(assets)
    # events_df = get_events_df(events)
    #skills_df = get_skills_df(skills)

    print("Writing to CSV...")
    # get csv of each card type  
    invest_df.to_csv("investigators.csv")
    #skills_df.to_csv("skills.csv")

    print("Process Complete!")


################################# Get URL's by card type ####################################

def get_urls_by_type():
    '''Child of main
       Scrapes arkhamdb and returns a list of urls pages containing card information
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

if __name__ == "__main__":

    main()

