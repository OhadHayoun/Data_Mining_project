"""

"""
# imports and requirements
import click
import sqlite3
from sqlite3 import Error
import mysql.connector

"""

pip install --editable .

"""

def create_connection(db_file = "market_scraper.db"):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return db_connection


@click.group()
def cli():
    # main function
    click.echo('---enters the main func----') # todo - activate the main.py file
    pass


@click.option('--table', type=click.Choice(['key_data', 'stock_performance',
                                           'stock_link_list', 'stock_screener']),
              help='this opthion prints the size of dta files', required = True)
@click.option('--arg', type=click.Choice(['symbol', 'id', 'date_time']),
              help='this opthion prints the size of dta files', required = False)
@click.command()
def print_data(table, arg="*"):
    click.echo("------ enter to print data command ------")
    cur = create_connection()
    cursor = cur.cursor()
    cursor.execute(f"SELECT {arg} FROM {table}")
    data = cursor.fetchall()
    print(f"this is the data from {table} table:")
    for row in data:
        print(list(row))
    return



@click.command()
@click.option('--table', type=click.Choice(['key_data', 'stock_performance',
                                           'stock_link_list', 'stock_screener']),
              help='this opthion prints the size of dta files', required = True)
def last_update(table):
    click.echo("--last update--")
    cur = create_connection()
    cursor = cur.cursor()
    cursor.execute(f"SELECT MAX(date_time) FROM {table} ")
    data = cursor.fetchall()
    print(f"The last update of {table} table:")
    for row in data:
        print(str(row))
    return



@click.command()
@click.option('--table', type=click.Choice(['key_data', 'stock_performance',
                                           'stock_link_list', 'stock_screener']),
              help='this option prints the size of data files', required = True)
def db_size(table):
    click.echo("--data base size--")
    cur = create_connection()
    cursor = cur.cursor()
    cursor.execute(f" USE {table};")
    data = cursor.fetchall()
    print(f"The size of {table} table:")
    for row in data:
        print(str(row))
    return


@click.command(help= "This command prints 'free style' queries")
@click.option('--table', required = True)
@click.option('--arg', required = True)
def print_fs(table, arg):
    cur =create_connection()
    cursor = cur.cursor()
    cursor.execute(f"SELECT {arg1} from {table};")
    data = cursor.fetchall()
    for row in data:
        print(row)
    return


cli.add_command(print_data)
cli.add_command(last_update)
cli.add_command(db_size)
cli.add_command(print_fs)


