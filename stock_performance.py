from bs4 import BeautifulSoup
import requests
import csv

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


##### main ####
def main():
    filename = 'stocks_links_list.csv'

    stocks_links_list = file_to_list(filename)
    print(stocks_links_list)

    rows = []
    rows.append(['Symbol', '5 Day ', '1 Month', '3 Month ', 'YTD', '1 Year'])

    for stock in stocks_links_list[:3]:
        symbol = stock[0]
        url = stock[1]

        url_check(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table', {'class': 'table table--primary no-heading c2'})

        if table is not None and len(table.find_all('li')) > 0:
            table_elements = table.find_all('li')
        else:
            print('performance table for {} not found'.format(symbol))
            continue

        elements_list = []
        elements_list.append(symbol)

        for i in range(0, len(table_elements), 2):
            try:
                elements_list.append(str(table_elements[i].getText()))
            except:
                print("loading performance table of {} failed".format(symbol))

        rows.append(elements_list)
        print(elements_list)

    write_file("stock performance", rows)



if __name__ == '__main__':
    main()

