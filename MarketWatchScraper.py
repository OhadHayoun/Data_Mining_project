"""

"""
# imports and requirements
import click
import os
import main as scraper
import stock_performance as sp
"""

pip install --editable .

"""

# class Config(object):
#
#     def __init__(self):
#         self.verbose = False

#pass_config = click.make_pass_decorator(Config)

@click.group()
def cli():
    # main function
    click.echo('---enters the main func----')
    pass


@click.command()
@click.option('--data', type=click.Choice(['full', 'Most_Active',
                                           'stock_p']))
def pd(data): # TODO - add different kinds of prints
    click.echo("------ enter to pd ------")
    if data == 'full': scraper.main(data)

    pass


@click.command()
@click.option('--path', default='Most Active.csv',
              help='this opthion prints the size of dta files')
def pds(path): # TODO - add last edit of file
    click.echo("----enter the print size data file ---")
    try:
        file_size= os.path.getsize(path)
    except OSError:
        print("----- YOU GOT PATH-SIZE-FILE PROBLEM -----")

    click.echo(f"---this size of default 'most active' file is --- {file_size/1000}kB")
    pass


@click.command()
#@click.option('--pfull', help='This option run the scraper and prints full output')
@click.option('--full', default='VVVVIKI****',
              help='This option run the scraper and print the output')
#@pass_config
def run(full):
    print("--------2 ----hello world".format(full))
    click.echo('hey- give me something %s' % full)



@click.command()
@click.option('--count', default =1, help='counts stuff')
@click.argument('name')
def func(count, name):
    click.echo(f"*** my name is {name}, and i love number {count}")


cli.add_command(pd)
cli.add_command(run)
cli.add_command(func)
cli.add_command(pds)
# run the scraper and print all scraper data

def print( ):
    """this script prints data"""
    pass

def get_data( ):
    """ this script gets the data """

    pass

def active_stocks( ):
    """ this script prints current most active stocks """
    pass


def timespane():
    """ gets the latest update """
    pass


