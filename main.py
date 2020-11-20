from bs4 import BeautifulSoup
import requests
import stock_performance as sp

def market_screener():
    """
    Get market data tables of 'Top gainers' and 'Most Active' stocks
    """

    #define  basic urls and required lists
    base_url = "https://www.marketwatch.com"

    url_dict = {'Top gainers': "https://www.marketwatch.com/tools/screener?mod=stocks",
                'Most Active': "https://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActive",
                }
    stocks_symbol_list = []
    stocks_links_list = []

    #itrate the url_dict to access each url
    for name, url in url_dict.items():
        sp.url_check(url)

        #getting a page request from the url and parsing
        # the page to a table with BeautifulSoup
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            table = soup.find('table')

            # if table is not None and len(table.find_all('tr')) > 0:
            table_elements = table.find_all('tr')

        except ResourceWarning:
            print("Error reading '{}' page from url: {}".format(name,url))

        rows = ['Symbol ', 'Company', 'Last', 'Change', '%_Change', 'Volume', '$_Traded', 'Description', 'Staff', 'Comments']

        #iterating the table row (stock) to gat the data
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

        print(rows)

        #writing the rows data to a file
        sp.write_file(name, rows)

    # writing the stocks links list to a file
    sp.write_file('stocks_links_list', stocks_links_list)


def main():
    market_screener()
    sp.stock_performance()
    sp.get_stock_financials()


if __name__ == '__main__':
    main()



