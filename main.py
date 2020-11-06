from bs4 import BeautifulSoup as soup
import requests
import urllib.request
import csv
from urllib.request import urlopen

def url_check(url):
    """
    Connecting and checking request status to url address
    """

    # getting url request
    print('Connecting to ',url)
    req_check = requests.get(url)

    # checking request status
    print('url request status = [{}]'.format(req_check.status_code))

    if req_check.status_code == requests.codes.ok:
        print('request OK')
    else:
        print('request error')
        exit()

    return

def write_file(url_name,rows):
    """
    Create csv named "url_name".csv and write rows to the file
    """
    output_file_name = '{}.csv'.format(url_name)

    print('\nWriting results to file..')
    try:
        with open(output_file_name,'w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(rows)
            print('file "{}" created suuccesfuly\n\n'.format(output_file_name))
    except:
        print('Error writing to file "{}" '.format(output_file_name))
        return




url_address1 = "https://www.marketwatch.com/tools/screener?mod=stocks"  ### Top gainers

url_address2= "https://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActive"  ### Most Active

url_dict = {'Top gainers':"https://www.marketwatch.com/tools/screener?mod=stocks",
            'Most Active':"https://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActive"
            }


for url_name, url_address in url_dict.items():  ## itrating through the url pages in the url_dict

    url_check(url_address)


    # query the website and return the html to the variable 'page'
    page = requests.get(url_address)
    # page = urlopen(url_address)

    # parse the html using beautiful soup and store in variable 'soup'
    soup = soup(page.content, 'html.parser')

    # find results within table (table_body)
    # table_body = soup.find_all('tbody')

    ########
    table = soup.find('table')

    if table is not None and len(table.find_all('tr'))>0:
        table_elements = table.find_all('tr')
    ########

    # table_elements = soup.find_all('tr')
    # print('Number of elements', (len(table_elements)-1))

    # create and write headers to a list
    rows = []
    rows.append(['Symbol ', 'Company', 'Last',	'Change','%_Change','Volume','$_Traded', 'Description', 'Staff', 'Comments'])

    for result in table_elements:
        try:
            # find all columns per result
            data = result.find_all('td')
            # check that columns have data
            if len(data) == 0:
                continue

            # write columns to variables
            Symbol = data[0].getText()
            company = data[1].getText()
            Last = data[2].getText()
            Change = data[3].getText()
            Change_percent = data[4].getText()
            Volume = data[5].getText()
            Traded = data[6].getText()

            # write each result to rows
            rows.append([Symbol, company, Last, Change, Change_percent, Volume, Traded])
        except:
            pass

    print(rows)

    # Create csv and write rows to output file
    write_file(url_name,rows)





def main():

    return

if __name__ == '__main__':
    main()
