# Arkham DB Web Scraping Project

## Description and Goal

The goal of this project is to develop a web scraping script to gather data on player cards from the Arkham Horror Living Card Game. Having this data in tabular form will give me a fun way to practice SQL commands while helping me perform more precise searches while choosing cards to use during the game. I also plan on undertaking a followup project where I use Tableau to explore how different factions in the game influence the games mechanics and card pool.

**Note:** This project has been rewritten from its original form. A few days after finishing the project the Arkham DB got some major updates to its code base causing much of the previous version’s scraper to break. This gave me a chance to revisit the project and make some improvements. The old code and method have been preserved in the file old_code. 

## Method

**get_player_cards.py**

1. Scrape URLs from search page, by card type, and add them to a list
2. For each URL request HTML from the corresponding page and parse result using BeautifulSoup
3. Search parsed results for individual card descriptors and return the information as a list
4. Add each descriptor as a value under the appropriate key in a dictionary and convert the dictionary to a dataframe
5. write the data frame to a cvs file 'player_cards.csv'

**prepare_card_data.py**

1. Contains optional cleaning functions for dataframe contained in 'player_cards.csv'

**Using These Scripts**

* To run 'get_player_cards' you will need access to the following libraries - requests, BeautifulSoup, pandas, and regex
* To run functions in 'prepare_card_data.py' you will need access to the following libraries - unicodedata, nltk, pandas, and regex

* Clone Repo into a local file
* Run 'get_player_cards.py' to get 'player_cards.csv'
* If 'player_cards.scv' is in your current directory, run 'prepare.py' to get 'cleaned_player_cards.csv' for a cleaner version of the data
* 'prepare_card_data.py' contains functions that you may find helpful when preparing data for your project. Feel free to use this code in your own project.  

## Opportunities for Further Improvement

**Hard Coding** - Due to the particulars of the website there were some areas where hardcoding values could not be avoided, such as the number of results pages to scrape url links from. As a result, maintaining the script after the site is updated with new cards will require a manual code adjustment, which is not ideal.

## Special Thanks

A big thank you to the wonderful folks at [Arkham DB](https://arkhamdb.com/) for making a great website, and not blocking my scraper!
