from bs4 import BeautifulSoup as soup
import requests
import csv

data_url = "https://www.marketwatch.com/tools/screener?mod=stocks"
data_html = requests.get(data_url).content
print(data_html)

content = soup(data_html, 'html.parser')
# print(content)
options_tables = content.find_all('table')
print(options_tables)


# find results within table
# table = soup.find('table', attrs={'class': 'tableSorter'})

# results = options_tables.find_all('tr')

# print('results', results)
# print('Number of results', len(results))

# create and write headers to a list 
rows = []
rows.append(['Symbol ', 'Company', 'Last',	'Change','%_Change','Volume','$_Traded', 'Description', 'Staff', 'Comments'])
print(rows)

for result in options_tables:
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




print(rows)

# Create csv and write rows to output file
with open('mwatch.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)


def main():
    print('Hello World!')

if __name__ == '__main__':
    main()
