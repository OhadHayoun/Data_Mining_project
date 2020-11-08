from bs4 import BeautifulSoup
import requests
import urllib.request
import csv
from urllib.request import urlopen
import stock_performance as sp


def url_check(url):
    """
    Connecting and checking request status to url address
    """
    # getting url request
    print('Connecting to ', url)
    req_check = requests.get(url)

    # checking request status
    print('url request status = [{}]'.format(req_check.status_code))

    if req_check.status_code == requests.codes.ok:
        print('request OK')
    else:
        print('request error')
        exit()

    return


def write_file(url_name, rows):
    """
    Create csv named "url_name".csv and write rows to the file
    """
    output_file_name = '{}.csv'.format(url_name)

    print('\nWriting results to file..')
    try:
        with open(output_file_name, 'w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(rows)
            print('file "{}" created suuccesfuly\n'.format(output_file_name))
    except:
        print('Error writing to file "{}" '.format(output_file_name))
        return



def market_screener():
    """
    Get market data tables of 'Top gainers' and 'Most Active' stocks
    """

    base_url = "https://www.marketwatch.com"

    url_dict = {'Top gainers': "https://www.marketwatch.com/tools/screener?mod=stocks",
                'Most Active': "https://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActive",
                }

    stocks_symbol_list = []
    stocks_links_list = []

    for name, url in url_dict.items():
        url_check(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table')

        if table is not None and len(table.find_all('tr')) > 0:
            table_elements = table.find_all('tr')

        rows = []
        rows.append(
            ['Symbol ', 'Company', 'Last', 'Change', '%_Change', 'Volume', '$_Traded', 'Description', 'Staff', 'Comments'])

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


                if symbol not in stocks_symbol_list and 'M' in volume: # adding the stock symbol to a list
                    stocks_symbol_list.append(symbol)
                    print('{} added to stocks_symbol_list'.format(symbol))

                rows.append([symbol, company, last, change, change_percent, volume,traded]) # write each result to rows
            except:
                pass

            link = result.find("a").get('href') # getting the stock pages url link

            if [base_url + link] not in stocks_links_list:  # adding the stock page url link to a list
                stocks_links_list.append([symbol,base_url + link])

        print(rows)
        write_file(name, rows)

    write_file('stocks_links_list', stocks_links_list)


def get_stock_financials(stocks_symbol_list):
    """ getting stock financials data """

    base_financials_url_part1 = "https://www.marketwatch.com/investing/stock/"
    base_financials_url_part2 = "/financials?mod=mw_quote_tab"


    for symbol in stocks_symbol_list:
        url = base_financials_url_part1 + symbol + base_financials_url_part2
        url_check(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('table', {'class': 'crDataTable'})

        if table is not None and len(table.find_all('tr')) > 0:
            table_elements = table.find_all('tr')
        else:
            print('Annual Financials table for {} not found'.format(symbol))
            continue

        rows = []
        rows.append(['Symbol', '5 Day ', '1 Month', '3 Month ', 'YTD', '1 Year'])

        elements_list = []
        elements_list.append(symbol)

        for i in range(0, len(table_elements)):
            try:
                elements_list.append(str(table_elements[i].getText()))
            except:
                print("loading performance table of {} failed".format(symbol))


        rows.append(elements_list)
        print(elements_list)

    return

def main():
    market_screener()
    sp.stock_performance()
    sp.get_stock_financials()

if __name__ == '__main__':
    main()



