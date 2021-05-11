#Job IDs:
# canopus 301eced29b3844e2b43ab6137871e216
# library and analog
libraryID = '83eff73ee6354c2da585ec5116d943aa'
analogID = '0b7329c9409b4d2381e63599a0f77038'
canopusID = '301eced29b3844e2b43ab6137871e216'

# Loading in Libraries
# import argparse
import requests
import os
import csv 
import json
import pandas as pd
from ecoNet import*
from pyMolNetEnhancer import*

# parser = argparse.ArgumentParser()
# parser.add_argument('task', help='GNPS Job ID')
# parser.add_argument('type', help='library, analog or canopus')
# args = parser.parse_args()

# Get jobs
# libraryMatch = getJob(libraryID, 'library')
# analogMatch = getJob(analogID, 'analog') 
# canopusMatch = getJob(canopusID, 'canopus')

#Writing df for testing
# libraryMatch.df.to_csv('libraryTest.csv')
# analogMatch.df.to_csv('analogTest.csv')
# canopusMatch.df.to_csv('canopusTest.csv')

# For testing without having to request files
libraryMatch = pd.read_csv('libraryTest.csv')
analogMatch = pd.read_csv('analogTest.csv')

gnpsMatches = [libraryMatch, analogMatch] # For testing
# gnpsMatches = [libraryMatch.df, analogMatch.df] # For real

gnpsNames = ['libraryInchikeys', 'analogInchikeys']
inchiDict = {}

for index, dataset in enumerate(gnpsMatches): 
    dataName = gnpsNames[index]
    inchi = dataset['INCHI']

    inchiClean = inchi.drop_duplicates().dropna()
    inchiDict[dataName] = inchiClean 

inchiAll = pd.concat(inchiDict).drop_duplicates(keep = 'first').dropna()
inchikeys = getInchiKeys(inchiAll)

inchikeys.inchiFrame.to_csv('inchikeytesting.csv')

inchikeySeries = inchikeys.inchiFrame[['InChIKey']]
inchikeySeries.to_csv('inchikey.csv')

# get_classification and make_classy_table from pyMolNetEnhancer
# queries and retrieves classyfire classifcations using InchiKey csv
get_classifications('inchikey.csv')

with open("all_json.json") as tweetfile:
    jsondic = json.loads(tweetfile.read())


df = make_classy_table(jsondic)

# Percent of inchikeys which could not be classyfied
len(set(list(inchikeys.inchiFrame.inchikey)) - set(list(df.inchikey)))/len(set(list(inchikeys.inchiFrame.inchikey)))



