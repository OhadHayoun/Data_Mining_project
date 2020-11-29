from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine
import re
import logging

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

    return


def df_to_db(database_name, table_name, df, option='append'):
    """
    uploading pandas DataFrame to the Database
    """
    # SQLAlchemy connectable
    engine = create_engine('sqlite:///{}.db'.format(database_name), echo=False)
    sqlite_connection = engine.connect()

    df.to_sql(table_name, sqlite_connection, if_exists=option, index=False)
    return


def db_to_df(database_name, table_name):
    """
    loading pandas DataFrame from the Database
    """
    # SQLAlchemy connectable
    engine = create_engine('sqlite:///{}.db'.format(database_name), echo=False)
    sqlite_connection = engine.connect()

    df = pd.read_sql_table(table_name, engine)

    return df


def value_to_float(value_string):
    """This function converts a string value containing ('$','K','M','B') to a float number:
     'K' = value *1000
     'M' = value *1,000,000
     'B' = value *1,000,000,000
     """
    if type(value_string) == float or type(value_string) == int:
        return value_string
    if value_string == 'N/A' or  value_string == 'None':
        return None

    if '$' in value_string:
        value_string = value_string.replace('$', '')

    if 'K' in value_string:
        if len(value_string) > 1:
            return int(''.join(re.findall(r'\d+', (value_string.replace('K', ''))))) * 1000
    if 'M' in value_string:
        if len(value_string) > 1:
            return int(''.join(re.findall(r'\d+', (value_string.replace('M', ''))))) * 1000000

    if 'B' in value_string:
        return int(''.join(re.findall(r'\d+', (value_string.replace('B', ''))))) * 1000000000
    else:
        return value_string

# def get_stock_financials():
#     """ getting stock financials data """
#
#     base_financials_url_part1 = "https://www.marketwatch.com/investing/stock/"
#     base_financials_url_part2 = "/financials?mod=mw_quote_tab"
#
#     filename = 'stocks_links_list.csv'
#     stocks_links_list = file_to_list(filename)
#
#     for stock in stocks_links_list:
#         symbol = stock[0]
#
#         url = base_financials_url_part1 + symbol + base_financials_url_part2
#
#         url_check(url)
#         try:
#             page = requests.get(url)
#             soup = BeautifulSoup(page.text, 'html.parser')
#             table = soup.find_all('tr')
#         except:
#             logging.warning('Annual Financials table for {} not found'.format(symbol))
#
#         rows = ['Description', '2015 ', '2016', '2017', '2018', '2019']
#
#         elements_list = []
#
#         # for i in range(1, len(table_elements)):
#         for i in table:
#
#             try:
#                 data = i.find_all('td')
#                 for value in data[:-1]:
#                     elements_list.append(str(value.getText()).strip())
#                 rows.append(elements_list)
#                 elements_list = []
#
#             except:
#                 logging.error("loading Financials table of {} failed".format(symbol))
#
#         print(rows)
#
#         # write_file(symbol + "_Financials", rows, 'Financials')
#         write_file(symbol + "_Financials", rows, 'Financials')
#
#     return


def stock_key_data():
    """
    scrapes the stock 'KEY DATA' and the 'PERFORMANCE' tables from the stock 'OVERVIEW' page
    """
    TABLE_NAME = 'stock_key_data'
    DB_NAME = 'market_scraper'

    links_df = db_to_df(DB_NAME, 'stocks_links_list')
    print(links_df)

    # filename = 'stocks_links_list.csv'
    # stocks_links_list = file_to_list(filename)
    rows = []

    for row in links_df.iterrows():
        symbol = row[1][0]
        url = row[1][1]

        # checking url and getting the page
        url_check(url)
        page = requests.get(url)

        # parsing the page with BeautifulSoup
        soup = BeautifulSoup(page.text, 'html.parser')

        # get the stock_performance data of the current stock symbol
        stock_performance(soup, symbol)

        # loading the required table value
        table = soup.find('ul', {'class': 'list list--kv list--col50'})

        # getting the table elements from the table
        if table is not None and len(table.find_all('li')) > 0:
            table_elements = table.find_all('li')
        else:
            logging.warning('performance table for {} not found'.format(symbol))
            continue

        elements_list = [symbol]
        columns_list = ['symbol']

        # iterating through the table elements and getting the required values
        for i in range(0, len(table_elements)):
            try:
                elements_list.append(str(table_elements[i].contents[3].getText()))
                columns_list.append(str(table_elements[i].contents[1].getText()))

            except ResourceWarning:
                logging.warning("loading performance table of {} failed".format(symbol))
            else:
                logging.info("performance table of {} loaded successfully".format(symbol))

        # remove '%' and convert percentage to float
        # [(float(x.strip('%')) / 100) if '%' in x else x for x in elements_list]
        # [x + '[%]'  if '%' in x else x for x in columns_list]

        # adding the values to the 'rows' table
        rows.append(elements_list)
        print(elements_list)

    # creating a pd DataFrame from the 'rows' table
    df = pd.DataFrame(rows, columns=columns_list)

    # converting string numbers columns to float (on selected columns list)
    convert_list = ['Open', 'Market Cap', 'Shares Outstanding', 'Public Float', 'Beta', 'Rev. per Employee',
                    'P/E Ratio', 'EPS', 'Yield', 'Dividend', 'Short Interest', 'Average Volume']
    for i in convert_list:
        try:
            df[i] = df[i].apply(value_to_float).astype(float)
        except:
            logging.warning("error converting '{}' from {} to float".format(symbol,TABLE_NAME))

    df['date_time'] = pd.to_datetime('now')

    # prints df for tests
    print(df)

    # uploading df to the database
    try:
        df_to_db(DB_NAME, TABLE_NAME, df)
        logging.info('df table {} uploaded to the database'.format(TABLE_NAME))
        print('df table {} uploaded to the database'.format(TABLE_NAME))

    except:
        print('uploading df table {} to the database failed'.format(TABLE_NAME))
        logging.ERROR('uploading df table {} to the database failed'.format(TABLE_NAME))

    return


def stock_profile():
    """
    scrapes the stock 'Profile' data from the Profile url page
    """
    TABLE_NAME = 'stock_profile'
    DB_NAME = 'market_scraper'

    base_financials_url_part1 = "https://www.marketwatch.com/investing/stock/"
    base_financials_url_part2 = "/company-profile?mod=mw_quote_tab"

    links_df = db_to_df(DB_NAME, 'stocks_links_list')

    rows = []

    for row in links_df.iterrows():
        symbol = row[1][0]
        url = base_financials_url_part1 + symbol + base_financials_url_part2


        # checking url and getting the page
        url_check(url)

        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            # loading the required table value
            table = soup.find('div', {'class': 'element element--text at-a-glance has-background background--blue'})
            table2 = soup.find_all('td')

        except ResourceWarning:
            logging.warning('Error parsing the stock profile page for {} not found'.format(symbol))

        else:
            # getting the table elements from the table
            if table is not None and len(table.find_all('li')) > 0:
                market = soup.find('span', {'class': "company__market"}).getText()

                company_market = market.split()[1]

                address_div = table.find('div', {'class': "address"})
                address = address_div.contents[1].contents[0] + ', ' + address_div.contents[3].contents[0]

                phone_div = table.find('div', {'class': "phone"})
                phone = phone_div.contents[3].getText()

                # getting the table elements from the table
                table_elements = table.find_all('li')

            else:
                logging.warning('Stock profile data for {} not found'.format(symbol))
                continue

            try:
                # profile index for specific values
                profile_index = [42, 43, 48, 49, 52, 53, 58, 59, 60, 61, 62, 63, 72, 73, 74, 75, 80, 81]

                # getting the values
                x = []
                for i in profile_index:
                    x.append(table2[i].getText())
                profile_cols, profile_values = x[::2], x[1::2]

            except:
                # except ResourceWarning:
                logging.warning('Error parsing the stock profile page for {}'.format(symbol))
            else:

                elements_list = [symbol, company_market, address, phone]
                columns_list = ['symbol', 'company_market', 'address', 'phone', 'Industry', 'Sector',
                                'Fiscal Year-end', 'Revenue', 'Net Income', 'Sales Growth', 'Employees',
                                'P/E Current', 'Price to Sales Ratio', 'Price to Cash Flow Ratio',
                                'Total Debt to Enterprise Value', 'Revenue/Employee', 'Income Per Employee', 'Cash Ratio', 'Gross Margin', 'Net Margin']

                # iterating through the table elements and getting the required values
                for i in range(0, len(table_elements)):
                    try:
                        elements_list.append(str(table_elements[i].contents[3].getText()))
                        # columns_list.append(str(table_elements[i].contents[1].getText()))
                    except:
                        logging.warning("loading performance table of {} failed".format(symbol))
                    else:
                        logging.info("performance table of {} loaded successfully".format(symbol))

                # adding the values to the 'rows' table
                rows.append(elements_list + profile_values)
                print(elements_list)

    # creating a pd DataFrame from the 'rows' table
    df = pd.DataFrame(rows, columns=columns_list)
    # df = pd.DataFrame(rows, columns=columns_list + profile_cols)

    # adding current datetime column
    df['date_time'] = pd.to_datetime('now')

    # prints df for tests
    print(df)

    # uploading df to the database
    try:
        df_to_db(DB_NAME, TABLE_NAME, df)
        logging.info('df table {} uploaded to the database'.format(TABLE_NAME))
        print('df table {} uploaded to the database'.format(TABLE_NAME))

    except:
        logging.ERROR('uploading df table {} to the database failed'.format(TABLE_NAME))
        print('uploading df table {} to the database failed'.format(TABLE_NAME))

    return


def stock_performance(soup, symbol):
    """
    scrapes the stock 'PERFORMANCE' table from the stock 'OVERVIEW' page
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
    columns_list = ['symbol', '5 Day[%]', '1 Month[%]', '3 Month[%]', 'YTD[%]', '1 Year[%]']

    # iterating through the table elements and getting the required values
    for i in range(0, len(table_elements), 2):
        try:
            element_value = str(table_elements[i].getText())
            if '%' in element_value:
                element_value = element_value.replace('%', '')
            elements_list.append(element_value)
            # columns_list.append(str(table.contents[i].contents[1].contents[1].getText()))
        except:
            logging.warning("loading performance table of {} failed".format(symbol))
        else:
            logging.info("performance table of {} loaded successfully".format(symbol))

    rows.append(elements_list)
    print(elements_list)

    # filling missing data with 'Nan'
    if len(rows[0]) < 6:
        for i in range(6-len(rows[0])):
            rows[0].append('Nan')

    # creating a pd DataFrame from the 'rows' table
    df = pd.DataFrame(rows, columns=columns_list)
    df['date_time'] = pd.to_datetime('now')

    # prints df for tests
    print(df)

    # uploading df to the database
    try:
        df_to_db(DB_NAME, TABLE_NAME, df)
        logging.info('df table {} uploaded to the database'.format(TABLE_NAME))
        print('df table {} uploaded to the database'.format(TABLE_NAME))

    except:
        logging.ERROR('uploading df table {} to the database failed'.format(TABLE_NAME))
        print('uploading df table {} to the database failed'.format(TABLE_NAME))

def main():
    stock_profile()
    stock_key_data()


if __name__ == '__main__':
    main()
