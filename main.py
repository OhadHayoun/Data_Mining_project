from bs4 import BeautifulSoup
import requests
import csv
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


def market_screener(command = None):
    print(command)
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


def main(command = None):
    market_screener(command)
    sp.stock_performance(command)
    sp.get_stock_financials(command)


if __name__ == '__main__':
    main()



