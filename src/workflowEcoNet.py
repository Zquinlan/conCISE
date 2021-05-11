#Job IDs:
# canopus 301eced29b3844e2b43ab6137871e216
# library and analog
libraryID = '83eff73ee6354c2da585ec5116d943aa'
analogID = '0b7329c9409b4d2381e63599a0f77038'
canopusID = '301eced29b3844e2b43ab6137871e216'

# Loading in Libraries
# import argparse
import requests
import json
import pandas as pd
from ecoNet import *
from pyMolNetEnhancer import *

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
inchiKeyDict = {}

for index, dataset in enumerate(gnpsMatches): 
    dataName = gnpsNames[index]
    inchi = dataset['INCHI']

    inchiClean = inchi.drop_duplicates().dropna()
    inchiKeyDict[dataName] = inchiClean
    # inchikeys = getInchiKeys(inchiClean)


    # inchikeys.inchiFrame.to_csv(str(dataName + 'Convert.csv'))
print(inchiKeyDict)
inchiKeyDict.info()
