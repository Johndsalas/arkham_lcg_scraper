# Arkham DB Web Scraping Project

## Description and Goal

The goal of this project is to develop a web scraping script to gather data on player cards from the Arkham Horror Living Card Game. The information will be scraped from Arkham DB and converted into four dataframes. (One for each card type) The data frames will be stored in separate csv files. Having this data in tabular form will give me a fun way to practice SQL commands while helping me perform more precise searches while choosing cards to use during the game. I also plan on undertaking a followup project where I use Tableau to explore how different factions in the game influence the games mechanics and card pool.

## Method

**main.py** - Scrapes URLs from search page by card type, calls functions from support files (invest.py, assets.py, events.py, and skills.py) to create data frames containing their respective card types, then writes the data frames to CSVs.

**invest.py, assets.py, events.py, skills.py** - Each use URL’s gathered from main to scrape information from individual cards and create a data frame of its type. Helper functions common to each are imported from help.py

**helper.py** - holds functions common to invest.py, assets.py, events.py, and skills.py to avoid repeating code.

## Using This Script 

* You will need access to the following Python libraries - requests, BeautifulSoup, pandas, re

* Clone Repo into a local file

* Run main.py to generate four csv files each containing information on a different card type (investigators, assets, events, and skills)

**File dependencies - main.py → invest.py, assets.py, events.py, skills.py → helper.py**

**You will need all files stored in the same file to run the script**

## Opportunities for Further Improvement

**Hard Coding** - Do to the particulars of the website there were some areas where hardcoding values could not be avoided, such as the number of results pages to scrape url links from. As a result, maintaining the script after the site is updated with new cards will require a manual code adjustment, which is not ideal.

**Code Organization** - Many of the card categories overlap and their “scrape commands” are the same so it may be possible to create one big dataframe using all of the possible values instead of using separate code for each card type. This would greatly condense the amount of code used in the project. Also, if I were to begin again I would have waited to perform minor cleaning until the scraper was capturing everything correctly. This would have allowed me to do the cleaning as one step instead of being distributed throughout the capture code. This would improve readability and reduce the amount of code needed.

**Though there were some missteps, I am overall happy with the result.**

## Special Thanks 

A big thank you to the wonderful folks at Arkham DB for making a great website, and not blocking my scraper!  
