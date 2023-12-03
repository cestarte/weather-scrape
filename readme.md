# weather-scrape

Scrape weather data from the web and store it into a local sqlite database.
Work in progress! Right now there's just a single source. Supply a wunderground URL and the script will collect the info and print it to your terminal. 

## Prerequisites

Install the required packages. This could be different based on your existing environment. If something is missing, let me know! Choose the install option below that's right for your environment.

**Conda Installs**

1. You should create a new conda environment for running this app.
1. Run `conda install --file installs.txt`

**Pip Installs**

Run `pip install -r installs.txt`


## Create the database

The app stores the scraped data into a database.

`python3 prepare_database.py`

To wipe it out and start over, use the `-d` argument.

## Run the app

`python3 main.py`


# Configure

The path to the  settings file is specified in `.env`. Open with a text editor if you need to relocate this file.

## Settings file

By default, the settings file is named `settings.json` and found in the local app directory. This file is used to specify the full path to the database and an array of the URLs to be collected.

# Rules

To prevent spamming, the app will check each URL and the date against the database before scraping that same data again. If it has already been collected today, it won't happen. You can add additional URLs to the settings without worrying about duplicate requests.