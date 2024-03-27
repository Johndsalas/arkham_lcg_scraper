'''Script for scraping palyer card information from arkham LCG website'''

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

################################################# scrape urls from website ################################################################

def get_urls():
    '''Returns a list of player card url's as strings''' 
       
    # calls get_cata_urls for each card type and extends urls to include all scraped urls 
    urls = []
    
    tipes = ['investigator','asset', 'event', 'skill']
    
    for tipe in tipes:
        
        print(f'Getting {tipe} URLs!')
        
        urls.extend(get_cata_urls(tipe))
        
    return urls


def get_cata_urls(catagory):
    ''' Takes in a string containing a player card faction, Scrapes arkhamdb, and
        Returns a list containing url's as strings for each card in that catagory'''

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
        urls = soup.find(id='list')

        urls = urls.find_all('a', class_='card-tip')

        # convert urls to string and make a list
        urls = [str(url['href']) for url in urls]
                
        full_results.extend(urls)
                
    return full_results

################################# Get request object for URL and parse using BeautifulSoup #################################################

def get_soup(url):
    '''Takes in a url as a string
       Calls get_text_for_icon to replace html that generates card icons with text reperesintationss
       Returns html request result parsed using beautiful soup'''

    # create request and soup objects
    html = requests.get(url)

    # locate urls on page and return
    soup = BeautifulSoup(html.content, 'html.parser')

    return soup

############################### Use URL to scrape card descriptors and creare a dataframe ##########################################################

def get_card_df(urls):
    '''Takes in urls for player cards and 
       Returns a df containing each cards information
       Catagories that do not apply to a given card are returned with a value of -- '''

    # dictionary with empty traits
    card_dict = {'title':[],
                 'faction':[],
                 'type':[],
                 'cost':[],
                 'traits':[],  
                 'ability':[],
                 'icons':[],  
                 'willpower':[],
                 'intellect':[],
                 'combat':[],
                 'agility':[],                       
                 'health':[],
                 'sanity':[],
                 'xp':[],
                 'artist':[],
                 'expansion':[],
                 'flavor':[],
                 'deck_building':[],
                 'story':[],
                 'url':[]}

    print("Getting cards...")

    # for each url get player card info from that page and add each element to descriptors
    for url in urls:

        # make html request to arkham db and parse using BS
        soup = get_soup(url)

        # parse soup for individual discriptors return as a list
        descriptors = get_card_info(soup)

        descriptors.append(url)

        print(f'Getting {descriptors[0]}') # print progress update to terminal

        # itterate through discriptor titles in dictionary and appent matching discriptor
        for i, key in enumerate(card_dict):

            card_dict[key].append(descriptors[i])

    print("Making dataframe...") # print update to terminal

    return pd.DataFrame(card_dict)


def get_card_info(soup):
    '''Takes in html request parsed by BeautifulSoup
       Returns a list of discriptors as strings for that card'''

    # parse soup for descriptors common to all card types
    # if element is not present in all cards use try except 
    # on except return -- for the value

    title = get_title(soup)

    faction = get_faction(soup)
    
    first_faction = faction.split(' ')[0] # for subsequent searches requiring faction

    tipe = soup.find('p', class_='card-type').text.replace('.','').replace('Hand x2','handx2').lower().strip()
    
    try:
    
        traits = soup.find('p', class_='card-traits').text.replace('Silver Twilight','SilverTwilight').replace('.','').lower().strip()
    
    except:
        
        traits = '--'
        
    ability = get_ability(soup, first_faction)

    artist = soup.find('div', class_='card-illustrator').text.replace('\n', '').replace('\t', '')

    expansion = soup.find('div', class_='card-pack').text.replace('\n', '').replace('\t', '').replace('.', '')

    flavor = get_flavor(soup)
    
    # get sets of descriptors not common to all card types set misssing values to "--"
    
    if tipe.split(' ')[0] in ('asset','event','skill'):
    
        icons = get_icons(soup)
    
        xp = get_xp(soup)
        
    else:
        
        icons = '--'
        
        xp = '--'
        
    if tipe.split(' ')[0] in ('asset','investigator'):
        
        health, sanity = get_health_sanity(soup)

    else:

        health = '--'

        sanity = '--'
            
    if tipe.split(' ')[0] in ('asset','event'):
        
        cost = get_cost(soup).strip()
                        
    else:
        
        cost = '--'
        
        
    if tipe.split(' ')[0] in ('investigator'):
        
        willpower = soup.find('li', title='Willpower').text.strip()

        intellect = soup.find('li', title='Intellect').text.strip()

        combat = soup.find('li', title='Combat').text.strip()

        agility = soup.find('li', title='Agility').text.strip()

        deck_building = get_text_for_icon(soup.find_all('div', class_=f'card-text border-{first_faction}')[1].text.replace('\n', '').replace('()','').replace('(, , , , or )', ''))

        story = get_story(soup)
        
    else:
        
        willpower = '--'
        intellect = '--'
        combat = '--'
        agility = '--'
        deck_building = '--'
        story = '--'

    return [title,
            faction,
            tipe,
            cost,
            traits,
            ability,
            icons,
            willpower,
            intellect,
            combat,
            agility,
            health,
            sanity,
            xp,
            artist,
            expansion,
            flavor,
            deck_building,
            story]


def get_title(soup): 
    '''Takes in html object parsed by BeautifulSoup
       Returns card title as a string'''
    
    title = soup.find('a', class_='card-name card-tip').text.replace('\n', '').strip()
    
    try:
        
        subtitle = f" {soup.find('div', class_='card-subname small').text.strip()}"
        
    except:
        
        subtitle = ''
    
    return title + subtitle


def get_faction(soup):
    '''Takes in html object parsed by BeautifulSoup
       Returns card faction as a string'''
    
    faction = ''

    for item in soup.find_all('div', class_='card-faction'):

        faction += item.text.replace('\n', ' ')

    return faction.lower().strip()


def get_health_sanity(soup):
    '''Takes in html object parsed by BeautifulSoup
       Returns health and sanity as a string'''

    try:
        
        health = re.search('Health:\s+(\d+)', str(soup.find('div'))).group(1).strip()
        
    except:
        
        health = '--'

    try:
        
        sanity = re.search('Sanity:\s+(\d+)', str(soup.find('div'))).group(1).strip()
        
    except:
        
        sanity = '--'

    return health, sanity


def get_ability(soup, first_faction):
    '''Takes in html object parsed by BeautifulSoup
       Returns card ability as a string'''
    
    soup = str(soup.find('div', class_=f'card-text border-{first_faction}'))
        
    soup = get_text_for_icon(soup)

    soup = re.sub(r'<[^<>]*>', '', soup)
        
    return soup


def get_flavor(soup):
    '''Takes in html object parsed by BeautifulSoup
       Returns card flavor text as a string'''
  
    flavor = soup.find('div', class_='card-flavor small').text.replace('\n', '').replace('\t', '')

    if flavor.strip() == '':
        
        flavor = '--'
        
    return flavor


def get_cost(soup):
    '''Takes in html object parsed by BeautifulSoup
       Returns card cost as a string'''
    
    text = str(soup.find_all('div', class_='card-info-block'))

    try:
    
        text = re.search('Cost:\s+(\d)', text).group(1)
        
    except:
        
        text = 'X'
        
    return text


def get_xp(soup):
    '''Takes in html object parsed by BeautifulSoup
       Returns card XP as a string'''
    
    text = str(soup.find_all('div', class_='card-info-block'))

    try:
        
        text = re.search('XP:\s+(\d)', text).group(1)
        
    except:
        
        text = '--'
        
    return text
    
    
def get_icons(soup):
    '''Takes in request results for an arkhamdb page containing player card data
        Returns a string represintation of test icons on the card'''
      
    icons = ''

    # list containing each icon type
    icon_types = ['wild', 'willpower', 'combat', 'agility', 'intellect']

    # itterate through icon types
    for stat in icon_types:

        # get number of that icon on card from request results
        num_icons = len(soup.find_all('span', class_=f'icon icon-large icon-{stat} color-{stat}'))

        # add that icon name to a string for each time it appears in request results
        for icon in range(num_icons):

            icons += f'{stat} '
            
    return icons.upper()[:-1]


def get_story(soup):
    '''Takes in html object parsed by BeautifulSoup
       Returns card XP as a string'''
    
    try:

        story = soup.find_all('div', class_='card-flavor small')[1].text.replace('\n', '').replace('\t', '')

    except:

        story = '--'

    return story

############################ Convert html of icons to text represintation and clean text #############################################

def get_text_for_icon(soup):
    '''Takes in request response as a string
       replaces html code indicating a game icon with a text representation
       Returns sting with replacements'''
    
    # replace icon html with matching word in all caps
    icon_types = ['action',
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
    
        soup = soup.replace(f'<span class="icon-{icon}" title="{icon.capitalize()}"></span>', f'{icon.upper()}')
        
        soup = soup.replace(f'<div class="card-text border-{icon}">\n<p>', '')

    soup = soup.replace(f'<span class="icon-wild" title="Any Skill"></span>', 'WILD')

    soup = soup.replace(f'<span class="icon-elder_sign" title="Elder Sign"></span>', 'ELDER_SIGN')

    soup = soup.replace(f'<span class="icon-elder_thing" title="Elder Thing"></span>', 'ELDER_THING')

    soup = soup.replace(f'<span class="icon-lightning" title="Fast Action"></span>', 'FAST_ACTION')

    soup = soup.replace(f'<span class="icon-auto_fail" title="Auto Fail"></span>', 'TENTACLES')

    return soup


if __name__ == '__main__':

    get_card_df(get_urls()).to_csv('player_cards.csv',index = False)


