import pandas
from sqlalchemy import create_engine

# filename = "C:\\Users\\liat grinberg\\Desktop\\Ohad\\ITC course\\Data_Mining_project\\Top gainers.csv"

filename = "Most Active.csv"
df = pandas.read_csv(filename)

print(df)

database_name = 'save_pandas'

engine = create_engine('sqlite:///market_scraper.db', echo=True)
sqlite_connection = engine.connect()

sqlite_table = "Top gainers"
df.to_sql(sqlite_table, sqlite_connection, if_exists='append')
