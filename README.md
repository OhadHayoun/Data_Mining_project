# Marketwatch Scraper

*this is a first version and this project is currently work-in-progress* 

This project is a financial data scraper, and it intended to generate data queries
from [www.marketwatch.com](www.marketwatch.com) \
our goal is to generate NYSE top stocks
and writes the main table into csv files \
---
### main.py
this scraper generates table data from  the following pages specified \
at the market_screener(): \
[top gainers of New York Stock Exchange](https://www.marketwatch.com/tools/screener?mod=stocks)  \
[most active of New York Stock Exchange](https://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActive) \
the data written to .csv file contains the following information:

* Symbol
* Company 
* Last
* Change
* % Change
* Volume
* $ Traded
* Description
* Staff
* Comments


#### Installations 
BeatifulSoup from bs4 \
requests \
urllib.request \
csv \
stock_performance 

---
### stock_performance.py
this scraper generates table data from different stocks specified
at the \
'stocks_links_list.csv' file (generated by main.py) \
and prints the financials performance of specified stocks during past years
into a .csv file

#### Installations
BeatifulSoup from bs4 \
requests \
csv

---



#### for more information and support:
please contact by email [ohadohad5@gmail.com](ohadohad5@gmail.com) and [chupavik@gmail.com](chupavik@gmail.com)



