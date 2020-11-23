#!/usr/bin/env python
"""  """

from setuptools import setup




setup(
    name='MarketWatchScraper',
    py_modules=['MarketWatchScraper'],
    install_requires=[
        'Click',
    ],
    entry_points='''
       [console_scripts]
       MarketWatchScraper=MarketWatchScraper:cli
       ''',
)


