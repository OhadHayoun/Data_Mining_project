from bs4 import BeautifulSoup
import requests
import csv
import os
import logging
import pandas as pd
from sqlalchemy import create_engine
import datetime

def file_to_list(filename):
    """
    receive a file name and return a list with the file's links
    """
    stocks_links_list = []

    with open(filename, 'r') as file:
        csvfile = csv.reader(file)
        if csvfile:
            for i, lines in enumerate(csvfile):
                if len(lines) < 1:
                    print("line {} error -> line skipped".format(i))

                elif (''.join(lines).strip()):
                    stocks_links_list.append([lines[0], lines[1]])
        else:
            print('Error - empty file')
            exit()

    return stocks_links_list

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
        logging.info('url request status = [{}]'.format(req_check.status_code))
    else:
        print('request error')
        logging.warning('Url request from {} Failed, '.format(url))
        exit()

    return

def write_file(url_name, rows, folder=None):
    """
    Create csv named "url_name".csv and write rows to the file
    """
    output_file_name = '{}.csv'.format(url_name)

    if folder:
        path = os.getcwd()
        if not os.path.isdir(folder):
            os.mkdir(folder)
        output_file_name = os.path.join(path, folder, output_file_name)

    print('\nWriting results to file..')

    try:
        with open(output_file_name, 'w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(rows)
            print('file "{}" created successfully\n'.format(output_file_name))
            logging.debug('file "{}" created successfully\n'.format(output_file_name))

    except FileExistsError:
        logging.error('Error writing to file "{}" '.format(output_file_name))
        return

def get_stock_financials():
    """ getting stock financials data """

    base_financials_url_part1 = "https://www.marketwatch.com/investing/stock/"
    base_financials_url_part2 = "/financials?mod=mw_quote_tab"

    filename = 'stocks_links_list.csv'
    stocks_links_list = file_to_list(filename)

    for stock in stocks_links_list:
        symbol = stock[0]

        url = base_financials_url_part1 + symbol + base_financials_url_part2

        url_check(url)
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            table = soup.find_all('tr')
        except:
            logging.warning('Annual Financials table for {} not found'.format(symbol))


        rows = ['Description', '2015 ', '2016', '2017', '2018', '2019']
        # rows.append(['Description', '2015 ', '2016', '2017', '2018', '2019'])

        elements_list = []

        # for i in range(1, len(table_elements)):
        for i in table:

            try:
                data = i.find_all('td')
                for value in data[:-1]:
                    elements_list.append(str(value.getText()).strip())
                rows.append(elements_list)
                elements_list = []

            except:
                logging.error("loading Financials table of {} failed".format(symbol))

        print(rows)

        # write_file(symbol + "_Financials", rows, 'Financials')
        write_file(symbol + "_Financials", rows, 'Financials')

    return

def stock_overview():
    """
    gets the stock 'KEY DATA' and the 'PERFORMANCE' tables from the stock 'OVERVIEW' page
    """
    TABLE_NAME = 'key_data'
    DB_NAME = 'market_scraper'

    filename = 'stocks_links_list.csv'
    stocks_links_list = file_to_list(filename)
    rows = []

    #iterating the stocks_links_list - each row the a stock page link
    for stock in stocks_links_list[:4]:   ###### 3 for test
        symbol = stock[0]
        url = stock[1]

        #checking url and getting the page
        url_check(url)
        page = requests.get(url)

        #parsing the page with BeautifulSoup
        soup = BeautifulSoup(page.text, 'html.parser')


        stock_performance(soup,symbol)

        #loading the required table value
        table = soup.find('ul', {'class': 'list list--kv list--col50'})

        #getting the table elements from the table
        if table is not None and len(table.find_all('li')) > 0:
            table_elements = table.find_all('li')
        else:
            logging.warning('performance table for {} not found'.format(symbol))
            continue

        elements_list = [symbol]
        columns_list = ['symbol']

        #iterating through the table elements and getting the required values
        for i in range(0, len(table_elements)):
            try:
                elements_list.append(str(table_elements[i].contents[3].getText()))
                columns_list.append(str(table_elements[i].contents[1].getText()))
            except ResourceWarning:
                logging.warning("loading performance table of {} failed".format(symbol))
            else :
                logging.info("performance table of {} loaded successfully".format(symbol))

        #adding the values to the 'rows' table
        rows.append(elements_list)
        print(elements_list)

    #creating a pd DataFrame from the 'rows' table
    df = pd.DataFrame(rows, columns=columns_list)
    df['date_time'] = pd.to_datetime('now')

    #prints df for tests
    print(df)

    #uploading df to the database
    df_to_db(DB_NAME, TABLE_NAME, df)

    # write_file("stock performance", rows)

    return

def stock_profile():
    return

def df_to_db(database_name, table_name, df):

    engine = create_engine('sqlite:///{}.db'.format(database_name), echo=False)
    sqlite_connection = engine.connect()

    df.to_sql(table_name, sqlite_connection, if_exists='append',index=False)
    return

def stock_performance(soup,symbol):
    """
    gets the stock 'PERFORMANCE' table from the stock 'OVERVIEW' page
    """
    TABLE_NAME = 'stock_performance'
    DB_NAME = 'market_scraper'

    rows = []

    table = soup.find('table', {'class': 'table table--primary no-heading c2'})

    if table is not None and len(table.find_all('li')) > 0:
        table_elements = table.find_all('li')
    else:
        logging.warning('performance table for {} not found'.format(symbol))

    elements_list = [symbol]
    columns_list = ['symbol','5 Day','1 Month','3 Month','YTD','1 Year']

    # iterating through the table elements and getting the required values
    for i in range(0, len(table_elements), 2):
        try:
            elements_list.append(str(table_elements[i].getText()))
            # columns_list.append(str(table.contents[i].contents[1].contents[1].getText()))
        except:
            logging.warning("loading performance table of {} failed".format(symbol))
        else:
            logging.info("performance table of {} loaded successfully".format(symbol))

    rows.append(elements_list)
    print(elements_list)

    #creating a pd DataFrame from the 'rows' table
    df = pd.DataFrame(rows, columns=columns_list)
    df['date_time'] = pd.to_datetime('now')

    #prints df for tests
    print(df)

    #uploading df to the database
    df_to_db(DB_NAME, TABLE_NAME, df)

# write_file("stock performance", rows)

def main():
    # stock_performance()
    # get_stock_financials()
    stock_overview()


if __name__ == '__main__':
    main()
