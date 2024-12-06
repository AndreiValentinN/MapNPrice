# Real Estate Interactive Dashboard

This program scrapes real estate listings, organizes them into an interactive dashboard, and integrates Google Maps for location-based distance calculations.  

## Features

- Scrapes real estate data (price, headline, location, and links).
- Displays data in a **Dash interactive table**.
- Allows users to view detailed information and calculate distances to property locations via Google Maps.
- Exports scraped data to a JSON file.

## Requirements

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver


## Install dependencies:
pip install -r requirements.txt

## Start the program:
run in console: python main.py



###The program will:

Open a browser to scrape real estate data from a pre-configured URL.
Export the results to results.json.
Launch an interactive Dash dashboard at http://127.0.0.1:8051.
In the dashboard:

Browse and filter property data.
Click on a property's location to view its distance from the user in Google Maps.