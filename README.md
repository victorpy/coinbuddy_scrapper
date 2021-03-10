# coinbuddy_scrapper
Python scrapper for coinbuddy

This is a scrapper for coinbuddy webpage. It uses beautifulsoup to look for crypto prices for different exchanges inside the page. After getting the prices, compares the differences, this is helpful for doing arbitrage. 

The coin_ref.py creates a csv file with the url of the coins that later, tables-exchanges-scrapper.py will scrap.
