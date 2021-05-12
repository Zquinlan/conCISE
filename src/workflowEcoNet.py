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
# This will need an in statement for analog math inclusion if ID != NA
# gnpsMatches = [libraryMatch.df, analogMatch.df] # For real

gnpsNames = ['libraryInchikeys', 'analogInchikeys']
smilesDict = {}

for index, dataset in enumerate(gnpsMatches): 
    dataName = gnpsNames[index]
    smiles = dataset['Smiles']

    smilesClean = smiles.drop_duplicates().dropna()
    smilesDict[dataName] = smilesClean 

# If statement for analog optional
smilesAll = pd.concat(smilesDict).drop_duplicates(keep = 'first').dropna()

#Convert Smiles to InchiKeys using PubChem
inchikeys = getInchiKeys(smilesAll)


inchikeySeries = inchikeys.inchiFrame[['InChIKey']]
inchikeySeries.columns = ['InChIKey']
inchikeySeries.to_csv('inchikey.csv')


# get_classification and make_classy_table from pyMolNetEnhancer
# queries and retrieves classyfire classifcations using InchiKey csv
get_classifier('inchikey.csv')

with open("all_json.json") as tweetfile:
    jsondic = json.loads(tweetfile.read())


gnpsClassyDf = make_classy_table(jsondic)

gnpsClassyDf = gnpsClassyDf.rename(columns = {'class':'CF_class','smiles':'SMILES'})
gnpsClassyDf.to_csv('gnpsClassyDf.csv')

