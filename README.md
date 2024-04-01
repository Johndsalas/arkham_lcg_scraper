# Arkham DB Web Scraping Project

## Description and Goal

The goal of this project is to develop a web scraping script to gather data on player cards from the Arkham Horror Living Card Game. The information will be scraped from Arkham DB and converted into four dataframes. (One for each card type) The data frames will be stored in separate csv files. Having this data in tabular form will give me a fun way to practice SQL commands while helping me perform more precise searches while choosing cards to use during the game. I also plan on undertaking a followup project where I use Tableau to explore how different factions in the game influence the games mechanics and card pool.

**Note:** This project has been rewritten from its original form. A few days after finishing the project the Arkham DB got some major updates to its code base causing much of the previous version’s scraper to break. This gave me a chance to revisit the project and make some improvements. The old code and method have been preserved in the file old_code. 

## Method

**aquire.py**

1. Scrapes URLs from search page by card type and form them into one list
2. For each URL request card make a request for information from that page and parse result using BeautifulSoup
3. Search parsed results for individual card descriptors and return the information as a list
4. Add each descriptor as a value under the appropriate key in a dictionary and convert the dictionary to a dataframe
5. write the data frame to a cvs file 'player_cards.csv'

**clean.csv**

1. Reads data from 'player_cards.csv'
2. Adds dummy columns for faction, type, and traits columns
1. cleans, tokenizes, and lemmatizes text in ability, story, and flavor columns
1. writes cleaned data to 'cleaned_player_cards.csv'

**File Dependencies**

* You must run 'aquire.py' and 'player_cards.csv' must be in your your current directory to run 'clean.csv'

**Using These Scripts**

* To run 'aquire.py' you will need access to the following libraries - requests, BeautifulSoup, pandas, and regex
* To run 'prepare.py' you will need access to the following libraries - unicodedata, nltk, pandas, and regex

* Clone Repo into a local file
* Run 'aquire.py' to get 'player_cards.csv'
* if 'player_cards.scv' is in your current directory, run 'prepare.py' to get 'cleaned_player_cards.csv'

## Opportunities for Further Improvement

**Hard Coding** - Due to the particulars of the website there were some areas where hardcoding values could not be avoided, such as the number of results pages to scrape url links from. As a result, maintaining the script after the site is updated with new cards will require a manual code adjustment, which is not ideal.

## Special Thanks

A big thank you to the wonderful folks at Arkham DB for making a great website, and not blocking my scraper!