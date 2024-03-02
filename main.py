'''Main script for scraping player card info from Arkhamdb website'''

# Imports
import requests
from bs4 import BeautifulSoup

from invest import get_invest_df
from assets import get_assets_df
from events import get_events_df
from skills import get_skills_df


def main():
    '''Scrapes Arkhamdb  
       Returns a dataframe containing player card information 
       by card type'''

    # get URL's by faction
    invest, assets, events, skills = get_urls_by_type()

    # get dataframe of each card type
    invest_df = get_invest_df(invest)
    skills_df = get_skills_df(skills)
    events_df = get_events_df(events)
    assets_df = get_assets_df(assets)
    
   

    print('Writing to CSV...')
    # get csv of each card type  
    invest_df.to_csv('investigators.csv')
    skills_df.to_csv('skills.csv')
    events_df.to_csv('events.csv')
    assets_df.to_csv('assets.csv')

    print("Process Complete!")


def get_urls_by_type():
    '''Scrapes arkhamdb and returns a list of urls pages containing card information
       on each card for each card type'''

    # call function to return list of url's by catagory
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
    ''' Takes in a string containing a player card faction, Scrapes arkhamdb, and
        Returns a list of urls for containing information on each card of that catagory'''

    full_results = []

    # defines number of results pages to scrape
    if catagory in ('investigator', 'skill'):
        
        pages = 1
        
    elif catagory == 'event':
        
        pages = 2
        
    elif catagory == 'asset':
        
        pages = 4

    # itterates through pages in catagory
    for page in range(1,pages+1):

        url = f'https://arkhamdb.com/find?q=t%3A{catagory}&view=list&sort=name&decks=player&page={page}'

        # create request and soup objects
        html = requests.get(url)

        soup = BeautifulSoup(html.content, 'html.parser')

        # locate urls on page
        results = soup.find(id='list')

        results = results.find_all('a', class_='card-tip')

        # convert urls to string and make a list
        results = [str(result['href']) for result in results]
                
        full_results.extend(results)
                
    return full_results


if __name__ == "__main__":

    main()