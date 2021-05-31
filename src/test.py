import numpy as np
# import json
# import pandas as pd
# from pyMolNetEnhancer import *
<<<<<<< HEAD
from ecoNet import *

job = '89c9d8b0a49d467390b70dd337bc7015'


# Requesting tsv output from GNPS API
test = getJob(job, 'edges')

weighted = weightEdges(test)

# test.df.to_csv('err/networkTest.csv')
=======
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
>>>>>>> f7d700461e1a5edd1ec5d8bfaa9229c570c9ad5c
