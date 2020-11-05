from bs4 import BeautifulSoup
import requests

data_url = "https://www.marketwatch.com/tools/screener?mod=stocks"
data_html = requests.get(data_url).content
print(data_html)

content = BeautifulSoup(data_html, 'html.parser')
# print(content)
options_tables = content.find_all('table')
print(options_tables)


def main():
    print('Hello World!')

if __name__ == '__main__':
    main()
