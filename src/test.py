import numpy as np
# import json
# import pandas as pd
# from pyMolNetEnhancer import *
# from ecoNet import *

# libraryMatch = pd.read_csv('libraryTest.csv')
# analogMatch = pd.read_csv('analogTest.csv')

# gnpsMatches = [libraryMatch, analogMatch] # For testing
# # gnpsMatches = [libraryMatch.df, analogMatch.df] # For real

# gnpsNames = ['libraryInchikeys', 'analogInchikeys']
# smilesDict = {}

# for index, dataset in enumerate(gnpsMatches): 
#     dataName = gnpsNames[index]
#     smiles = dataset['Smiles']

#     smilesClean = smiles.drop_duplicates().dropna()
#     smilesDict[dataName] = smilesClean 

# # If statement for analog optional
# smilesAll = pd.concat(smilesDict).drop_duplicates(keep = 'first').dropna()

# #Convert Smiles to InchiKeys using PubChem
# inchikeys = getInchiKeys(smilesAll)


# inchikeySeries = inchikeys.inchiFrame[['InChIKey']]
# inchikeySeries.columns = ['InChIKey']
# inchikeySeries.to_csv('inchikeyTest.csv')

# print(inchikeys)

print(np.isnan('asdfa'))