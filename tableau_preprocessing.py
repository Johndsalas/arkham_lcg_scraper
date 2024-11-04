''' Script for preprocessing data scraped from arkhamdb for 'By the Numbers' Tableau project '''

import pandas as pd
def get_tableau_data():
    
    # read in data from csv
    df = pd.read_csv('player_cards.csv')

    # fill nulls in icons with -- 
    df['icons'] = df['icons'].fillna('no_icons')

    # add iconc count columns
    icons = ['INTELLECT',
             'COMBAT',
             'AGILITY',
             'WILLPOWER',
             'WILD']

    for icon in icons:

        df[f'{icon.lower()}_count'] = df['icons'].str.count(icon)

     # dropping unused columns
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

    # replace -- in xp with 0 
    df['xp'] = df.xp.apply(lambda value : 0 if value == '--' else value)

    # drop weakness cards
    df = df[~df['type'].str.contains("weakness")]

    # drop duplicates
    df = df.drop_duplicates()

    return df


if __name__ == '__main__':

    get_tableau_data().to_csv('by_the_numbers.csv', index=False)