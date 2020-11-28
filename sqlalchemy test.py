from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,Float,DateTime
import logging
import os.path

#checks if database file already exists
if os.path.isfile('market_scraper.db'):
   print("Database File 'market_scraper.db' exist")
else:
   print("Database File 'market_scraper.db' not exist  -> creating new Database file..")

   engine = create_engine('sqlite:///market_scraper.db', echo = True)
   meta = MetaData()

   tables_names = ['stock_performance','stocks_links_list','stocks_screener','stock_profile','stock_key_data']

   stock_performance = Table(
      'stock_performance', meta,
      Column('id', Integer, primary_key = True, autoincrement=True),
      Column('symbol', String),
      Column('5 Day[%]', String),
      Column('1 Month[%]', String),
      Column('3 Month[%]', String),
      Column('YTD[%]', String),
      Column('1 Year[%]', String),
      Column('date_time', DateTime)
   )


   stocks_links_list = Table(
      'stocks_links_list', meta,
      Column('id', Integer, primary_key = True, autoincrement=True),
      Column('symbol', String),
      Column('url', String),
      Column('date_time', DateTime)
   )

   stocks_screener = Table(
      'stocks_screener', meta,
      Column('id', Integer, primary_key = True, autoincrement=True),
      Column('symbol', String),
      Column('company', String),
      Column('last_price', Float),
      Column('price_change', Float),
      Column('change_percentage', String),
      Column('volume', Float),
      Column('pe_ratio', Float),
      Column('market_cap', Float),
      Column('date_time', DateTime)
   )

   stock_profile = Table(
      'stock_profile', meta,
      Column('id', Integer, primary_key = True, autoincrement=True),
      Column('symbol', String),
      Column('company_market', String),
      Column('address', String),
      Column('phone', String),
      Column('Industry', String),
      Column('Sector', String),
      Column('Fiscal Year-end', String),
      Column('Revenue', Float),
      Column('Net Income', Float),
      Column('2019 Sales Growth', String),
      Column('Employees', Integer),
      Column('P/E Current', Float),
      Column('Price to Sales Ratio', Float),
      Column('Price to Cash Flow Ratio', Float),
      Column('Total Debt to Enterprise Value', Float),
      Column('Revenue/Employee', Float),
      Column('Income Per Employeee', Float),
      Column('Cash Ratio', Float),
      Column('Gross Margin', String),
      Column('Net Margin', String),
      Column('date_time', DateTime)
   )


   stock_key_data = Table(
      'stock_key_data', meta,
      Column('id', Integer, primary_key = True, autoincrement=True),
      Column('symbol', String),
      Column('Open', Float),
      Column('Day Range', String),
      Column('52 Week Range', String),
      Column('Market Cap', Float),
      Column('Shares Outstanding', Float),
      Column('Public Float', Float),
      Column('Beta', Float),
      Column('Rev. per Employee', Float),
      Column('P/E Ratio', Float),
      Column('Employees', String),
      Column('P/E Current', String),
      Column('EPS', Float),
      Column('Yield', Float),
      Column('Dividend', Float),
      Column('Ex-Dividend Date', String),
      Column('Short Interest', Float),
      Column('% of Float Shorted', String),
      Column('Average Volume', Float),
      Column('date_time', DateTime)
   )

   meta.create_all(engine)

   logging.info("database '{}' created ,\n tables names: {}" .format('market_scraper',tables_names))
   print("database '{}' created ,\n tables names: {}" .format('market_scraper',tables_names))

