from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import pandas as pd
import numpy as np
import requests

import os


def parseArticleTables(url):
    """ Parses article into table soups
        returns a list of tables as Beautifulsoup objects
     """
    
    # Parse url into tables
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')
    # print status
    print(f"Found { len(tables) } tables at given url.")

    return tables


def extractTableData(table):
    """ Returns a rows x cols dateframe of the wikitable """
    
    # Extract row data
    rows = table.find_all('tr')
    row_data = [td.text for td in rows]
    table_data = [text.splitlines() for text in row_data]
    df = pd.DataFrame(table_data[1:], columns=table_data[0])

    return df


def extractTablesData(tables):
    """ Returns a list of dfs """
    return [extractTableData(table) for table in tables]



def getWikiDfs(url):
    """ Takes in an article url and yeilds the found tables as DF:s """
    tables = parseArticleTables(url)
    dfs = extractTablesData(tables)

    return dfs


# Article url (possibly containing lists)
url = "https://sv.m.wikipedia.org/wiki/Lista_%C3%B6ver_matsvampar"
# tables = parseArticleTables(url)
# dfs = extractTablesData(tables)

dfs = getWikiDfs(url)
print(dfs)




def generateFileName(url):
    url_suffix = url.split('/')[-1]
    filename = unquote(url_suffix)
    return filename

# Export as csv:s
def exportDfs(dfs, url, method='csv'):
    """ Exports a lists of df:s as """

    # touches data dir in given path (current if no path given)
    if not os.path.exists('data'):
        os.makedirs('data')
    else:
        print("Exporting to /data")


    # Export
    for counter, df in enumerate(dfs, 1):
        path = os.path.join('data', generateFileName(url) + f'_{counter}')
        df.to_csv(path_or_buf=path)

    return

exportDfs(dfs, url)
