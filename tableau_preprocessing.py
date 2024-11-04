''' Script for preprocessing data scraped from arkhamdb for 'By the Numbers' Tableau project '''

import pandas as pd

def get_tableau_data():
    
    # read in data from csv
    df = pd.read_csv('player_cards.csv')

    # drop weakness cards
    df = df[~df['type'].str.contains("weakness")]

    # drop cards belonging to more than one faction
    df = df[df.faction.isin(['seeker', 
                             'mystic', 
                             'guardian', 
                             'survivor', 
                             'rogue', 
                             'neutral'])]

    # drop duplicates based on relevant columns
    df = df.drop_duplicates(subset=df.drop(columns=['url',
                                                    'artist', 
                                                    'expansion', 
                                                    'flavor',
                                                    'story']).columns)

     # add iconc count columns
    icons = ['INTELLECT',
             'COMBAT',
             'AGILITY',
             'WILLPOWER',
             'WILD']

    for icon in icons:

        df[f'{icon.lower()}_count'] = df['icons'].str.count(icon)

    # get dummy columns for cards included in each faction
    factions = ['seeker', 
                'mystic', 
                'guardian', 
                'survivor', 
                'rogue', 
                'neutral']

    for faction in factions:

        df[f'{faction}'] = df['faction'].str.contains(faction).astype(int)

    # fill nulls in icons with -- 
    df['icons'] = df['icons'].fillna('no_icons')

    # replace -- in xp with 0 
    df['xp'] = df.xp.apply(lambda value : 0 if value == '--' else value)

    # split type into type and slot and clean slot values
    df[['type', 'slot']] = df['type'].str.split(' ', n=1, expand=True)
    
    
    df['slot'] = df.slot.apply(clean_slot_text)

    # dropping columns not featured in report
    df = df.drop(columns = ['title', 
                            'icons',
                            'traits', 
                            'ability', 
                            'artist', 
                            'expansion', 
                            'flavor', 
                            'deck_building', 
                            'story', 
                            'url'])

    return df

def clean_slot_text(value):
    ''' takes in a pandas value from slot column
        returns cleaned value '''

    if value == None:

        return 'no slot'

    elif value == 'arcane x2':

        return 'arcanex2'
    
    else:

        return value.replace(' ', ' and ')


if __name__ == '__main__':

    get_tableau_data().to_csv('by_the_numbers.csv', index=False)