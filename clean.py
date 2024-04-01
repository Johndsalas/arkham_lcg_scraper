''' Script for cleaning data scraped using file main.py '''

import pandas as pd
import unicodedata
import regex as re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
nltk.download('stopwords')

############################################### Main cleaning function ################################################################

def full_clean():
    ''' Clean data scraped using scraper in main.py '''

    df = pd.read_csv('player_cards.csv')

    # get dummy columns for columns with space seperated variables
    for col in ['faction','type', 'traits']:

        df = get_space_dummies(df, col)

    for col in ['ability','story', 'flavor']:

        df = prep_description(df, col)

    return df

#################### Encode variables with cell values that contain multiple space seperated values ##################################

def get_space_dummies(df, col):
    '''Takes in a dataframe and a column name as a string
       Column chould contain cells with multiple space seperated values 
       Returns dataframe with encoded column values (True/False) for each value in the original column '''
    # get list of column values
    column_values = set(df[f'{col}'].tolist())

    split_values = []

    # split values containing multiple items and add to list
    for item in column_values:

        split_values.extend(item.split(' '))

    # get set of stripped values 
    cats = set(item.strip() for item in split_values if item != '')
    
    # get dummy column for each item 
    for cat in cats:
    
        df[f'{cat}_{col}'] = df[f'{col}'].apply(lambda value: cat in value)
        
    return df

############################################## Clean text columns ############################################################################### 

def prep_description(df, col):
    ''' Takes in a dataframe and column name with text values as a string
        Returns a dataframe with column texed cleaned and ready for analysis '''
    
    # merge words seperated by _
    df[f'{col}'] = df[f'{col}'].apply(lambda value: value.replace('_', ''))

    # convert strings to lowercase
    df[f'{col}'] = df[f'{col}'].apply(lambda value: str(value).lower())

    # remove special characters from description text
    df[f'{col}'] = df[f'{col}'].apply(lambda value: re.sub(r'[^\w\s]|[\d]', ' ', value))

    # remove non-ascii characters from description text 
    df[f'{col}'] = df[f'{col}'].apply(lambda value: unicodedata.normalize('NFKD', value)
                                                               .encode('ascii', 'ignore')
                                                               .decode('utf-8', 'ignore'))
    # tokenizes text in description
    df = get_disc_tokens(df, col)

    # lemmatize the text in description
    df[f'{col}'] = df[f'{col}'].apply(lemmatizer)

    # remove stopwords and words with less than three letters from text in description
    # return a list of words in the text

    df[f'{col}'] = df[f'{col}'].apply(remove_stopwords)

    return df


def get_disc_tokens(df, col):
    '''Tokenize text in descriptions column of a pandas data frame'''

    tokenizer = ToktokTokenizer()

    # tokenize text in description
    df[f'{col}'] = df[f'{col}'].apply(lambda value: tokenizer.tokenize(value, return_str=True))

    return df


def lemmatizer(value):
    '''Takes in a value from a pandas column and returns the value lemmatized'''

    # create lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()

    # get list of lemmatized words in value
    value_lemmas = [wnl.lemmatize(word) for word in value.split()]

    # turn list or words back into a string and return value
    return ' '.join(value_lemmas)


def remove_stopwords(value):
    ''' remove stopwords from text'''

    # get list of english language stopwords list from nlt
    stop_words = nltk.corpus.stopwords.words('english')

    # split words in pandas value into a list and remove words from the list that are in stopwords or less than 3 letters
    value_words = value.split()
    filtered_list = [word for word in value_words if (word not in stop_words) and (len(word) >= 3)]

    # convert list back into string and return value
    return ' '.join(filtered_list)


if __name__ == '__main__':

    full_clean().to_csv('cleaned_player_cards.csv', index = False)