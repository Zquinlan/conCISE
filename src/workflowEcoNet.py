#Job IDs:
# Moorea  
# libraryID = '16616afa8edd490ea7e50cc316a20222'
# analogID = '752f22be3e0746e1b0c4987acbc24d53'

# Pseudo-nitzchia
libraryID = '89c9d8b0a49d467390b70dd337bc7015'
analogID = '5c635e079c5a4eccbdcc7602eef88fc8'
canopusID = '301eced29b3844e2b43ab6137871e216'

# Loading in Libraries
# import argparse
import requests
import os
import pandas as pd
from ecoNet import*

# Get jobs
# N/A was added to the superclass. Filter for that
print('Getting GNPS jobs...')
libraryMatch = getJob(libraryID, 'library')
analogMatch = getJob(analogID, 'analog')  #change to if analog supplied
canopusMatch = getJob(canopusID, 'canopus')
edgeInfo = getJob(libraryID, 'edges')

# Morea CANOPUS job
# canopusMatch = pd.read_csv('~/Documents/SDSU_Scripps/EcoNet/investigations/canopus_summary.csv') 

# for non testing add .df to libraryMatch and analogMatch
librarySubset = libraryMatch.df[['#Scan#', 'superclass', 'class', 'subclass']].add_suffix('_library').rename(columns={'#Scan#_library': 'scan'})
if isinstance(analogMatch.df, pd.DataFrame):
    analogSubset = analogMatch.df[['#Scan#', 'superclass', 'class', 'subclass']].add_suffix('_analog').rename(columns={'#Scan#_analog': 'scan'})

canopusSubset = canopusMatch.df[['scan', 'superclass', 'class', 'subclass']].add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})

# Merge library, analogs and 
print(' ')
print('merging annotations...')
network = makeNet(edgeInfo)
merged = mergeAnnotations(librarySubset, canopusSubset, network.networks, analog = analogSubset)

print(' ')
print('Weighting nodes by relative cosine score...')
weights = None
weights = weightEdges(edgeInfo)


# Printing to CL for user
print(' ')
print('finding consensus annotations...')
# Propogate annotations
if not weights == None:
    annotations = selectAnnotation(merged.library, merged.insilico, network.networks, weights.edgeWeightings, analogWeight = True)

if weights == None:
    annotations = selectAnnotation(merged.library, merged.insilico, network.networks, analogWeight = True, edgeWeights = None)

annotations.export.to_csv('ecoNetConsensus.csv')

# Caluculating %consensus
numLibrary = len(annotations.export[annotations.export['matchSource'] == 'Library'].dropna(subset = ['ecoNetConsensus'])[['network']].drop_duplicates())
totalLibrary = len(merged.library[merged.library['superclass_library'].notna() == True][['network']].drop_duplicates())
numInsilico = len(annotations.export[annotations.export['matchSource'] == 'Insilico'].dropna(subset = ['ecoNetConsensus'])[['network']].drop_duplicates())
totalInsicilo = len(merged.insilico[merged.insilico['superclass_canopus'].notna() == True][['network']].drop_duplicates())


libraryConsensus = numLibrary/totalLibrary
insilicoConsensus = numInsilico/totalInsicilo
# Reporting success rate for consensus sequences
print(' ')
print(str(str(numLibrary) + " out of " + str(totalLibrary) + " (" + str(round(libraryConsensus, 4)*100) + "%)" + " networks with Library ID's found a consensus annotation"))
print(str(str(numInsilico) + " out of "  + str(totalInsicilo) + " (" + str(round(insilicoConsensus, 4)*100) + "%)" +  " networks with Insilico annotations found a consensus annotation"))





