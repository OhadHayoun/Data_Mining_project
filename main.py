from bs4 import BeautifulSoup
import requests
import stock_performance as sp
import pandas as pd
import logging

#Old function
def market_screener(command = None):
    print(command)
    """
    Get market data tables of 'Top gainers' and 'Most Active' stocks
    """

    # define  basic urls and required lists
    base_url = "https://www.marketwatch.com"

    url_dict = {'Top gainers': "https://www.marketwatch.com/tools/screener?mod=stocks",
                'Most Active': "https://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActive",
                }

    stocks_symbol_list = []
    stocks_links_list = []

    # itrate the url_dict to access each url
    for name, url in url_dict.items():
        sp.url_check(url)
        # getting a page request from the url and parsing
        # the page to a table with BeautifulSoup
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            table = soup.find('table')

            # if table is not None and len(table.find_all('tr')) > 0:
            table_elements = table.find_all('tr')

        except ResourceWarning:
            print("Error reading '{}' page from url: {}".format(name, url))

        rows = [['Symbol ', 'Company', 'Last', 'Change', '%_Change', 'Volume', '$_Traded']]

        # iterating the table row (stock) to gat the data
        for result in table_elements:
            try:
                # find all columns per result
                data = result.find_all('td')
                # check that columns have data
                if len(data) == 0:
                    continue

                # write columns to variables
                symbol = data[0].getText()
                company = data[1].getText()
                last = data[2].getText()
                change = data[3].getText()
                change_percent = data[4].getText()
                volume = data[5].getText()
                traded = data[6].getText()

                # adding the stock symbol to a list
                if symbol not in stocks_symbol_list and 'M' in volume:
                    stocks_symbol_list.append(symbol)
                    print('{} added to stocks_symbol_list'.format(symbol))

                # append each result to rows
                rows.append([symbol, company, last, change, change_percent, volume, traded])

            except ResourceWarning:
                print('Error getting  "{}" data'.format(result))

            # getting the stock pages url link
            link = result.find("a").get('href')

            # adding the stock page url link to a list
            if [base_url + link] not in stocks_links_list:
                stocks_links_list.append([symbol, base_url + link])

        print("==================")
        print(f"{name} OUTPUT")

        for row in rows:
            print(row)
        #writing the rows data to a file
        if command == None:
            sp.write_file(name, rows)

    # writing the stocks links list to a file
    if command == 'full':
        print("Stocks Links List:")
        for link in stocks_links_list:
            print(link)
    if command == None:
        sp.write_file('stocks_links_list', stocks_links_list)

#new function
def stocks_screener(command = None):
    print('command = ', command)
    """
    Get market data tables of stocks screener filter
    
    screener details:
    stocks
    volume > 1M
    market capitalization > 100M
    exchange = all [NYSE, NASDAQ, AMEX]
    industry = all
    """

    TABLE_NAME = 'stocks_screener'
    DB_NAME = 'market_scraper'

    name = 'stocks screener'
    exchange_list_options = ['all', 'NYSE', 'NASDAQ', 'AMEX']

    base_url = "https://www.marketwatch.com"

    url = 'https://www.marketwatch.com/tools/stockresearch/screener/results.asp?submit=Screen&Symbol=true&' \
          'Symbol=false&ChangePct=true&ChangePct=false&FiftyTwoWeekLow=false&' \
          'CompanyName=true&CompanyName=false&Volume=true&Volume=false&' \
          'PERatio=true&PERatio=false&Price=true&Price=false&LastTradeTime=false' \
          '&MarketCap=true&MarketCap=false&Change=true&Change=false&FiftyTwoWeekHigh=false' \
          '&MoreInfo=false&SortyBy=ChangePct&SortDirection=Descending&ResultsPerPage=Fifty&' \
          'TradesShareEnable=false&TradesShareMin=&TradesShareMax=&' \
          'PriceDirEnable=falsePriceDir=Up&PriceDirPct=&LastYearEnable=false&' \
          'LastYearAboveHigh=&TradeVolEnable=true&TradeVolMin=1000000&TradeVolMax=&' \
          'BlockEnable=false&BlockAmt=&BlockTime=&PERatioEnable=false&PERatioMin=&' \
          'PERatioMax=&MktCapEnable=true&MktCapMin=100&MktCapMax=&MovAvgEnable=false&' \
          'MovAvgType=Outperform&MovAvgTime=FiftyDay&MktIdxEnable=false&' \
          'MktIdxType=Outperform&MktIdxPct=&MktIdxExchange=&Exchange=All' \
          '&IndustryEnable=false&Industry=Accounting'


    'https://www.marketwatch.com/tools/stockresearch/screener/results.asp?submit=Screen&Symbol=true&Symbol=false&ChangePct=true&ChangePct=false&FiftyTwoWeekLow=false&CompanyName=true&CompanyName=false&Volume=true&Volume=false&PERatio=true&PERatio=false&Price=true&Price=false&LastTradeTime=false&MarketCap=true&MarketCap=false&Change=true&Change=false&FiftyTwoWeekHigh=false&MoreInfo=false&SortyBy=ChangePct&SortDirection=Descending&ResultsPerPage=Fifty&TradesShareEnable=false&TradesShareMin=&TradesShareMax=&PriceDirEnable=false&PriceDir=Up&PriceDirPct=&LastYearEnable=false&LastYearAboveHigh=&TradeVolEnable=true&TradeVolMin=1000000&TradeVolMax=&BlockEnable=false&BlockAmt=&BlockTime=&PERatioEnable=false&PERatioMin=&PERatioMax=&MktCapEnable=true&MktCapMin=100&MktCapMax=&MovAvgEnable=false&MovAvgType=Outperform&MovAvgTime=FiftyDay&MktIdxEnable=false&MktIdxType=Outperform&MktIdxPct=&' \
    'MktIdxExchange=&Exchange=NYSE&IndustryEnable=false&Industry=Accounting'

    #select exchange - dafault = all
    selected_exchange = exchange_list_options[0]
    url = url.replace("Exchange=All", "Exchange={}".format(selected_exchange))
    print(url[-58:-30])   #test

    sp.url_check(url)

    # getting a page request from the url and parsing
    # the page to a table with BeautifulSoup
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table')

        # if table is not None and len(table.find_all('tr')) > 0:
        table_elements = table.find_all('tr')

    except ResourceWarning:
        print("Error reading page from url: {}".format(url))

    stocks_symbol_list = []
    stocks_links_list = []
    rows = []
    columns_list = ['symbol', 'company', 'last_price', 'price_change', 'change_percentage', 'volume', 'pe_ratio', 'market_cap']



    # iterating the table row (stock) to gat the data
    for result in table_elements:
        try:
            # find all columns per result
            data = result.find_all('td')
            # check that columns have data
            if len(data) == 0:
                continue

            # write columns to variables
            symbol = data[0].getText()
            company = data[1].getText()
            last_price = data[2].getText()
            price_change = data[3].getText()
            change_percentage = data[4].getText()
            volume = data[5].getText()
            pe_ratio = data[6].getText()
            market_cap = data[7].getText()


            # adding the stock symbol to a list
            if symbol not in stocks_symbol_list:
                stocks_symbol_list.append(symbol)
                print('{} added to stocks_symbol_list'.format(symbol))

            # append each result to rows
            rows.append([symbol, company, last_price, price_change, change_percentage, volume, pe_ratio, market_cap])
            print(rows)

        except ResourceWarning:
            logging.warning('Error getting  "{}" data'.format(result))

        else:
            # getting the stock pages url link
            link = result.find("a").get('href')

            # adding the stock page url link to a list
            if [base_url + link] not in stocks_links_list:
                stocks_links_list.append([symbol, base_url + link])


    # creating a pd DataFrame from the 'rows' table
    df = pd.DataFrame(rows, columns=columns_list)
    df['date_time'] = pd.to_datetime('now')

    # prints df for tests
    print(df)

    # uploading df to the database
    sp.df_to_db(DB_NAME, TABLE_NAME, df)

    print("==================")
    print(f"{name} OUTPUT")

    for row in rows:
        print(row)
    # writing the rows data to a file
    if command == None:
        sp.write_file(name, rows)

    # writing the stocks links list to a file
    if command == 'full':
        print("Stocks Links List:")
        for link in stocks_links_list:
            print(link)
    if command == None:
        sp.write_file('stocks_links_list', stocks_links_list)

    return

def table_to_db():

    return

def main(command = None):
    stocks_screener(command)
    sp.stock_overview()
    # sp.get_stock_financials()


if __name__ == '__main__':
    main()



