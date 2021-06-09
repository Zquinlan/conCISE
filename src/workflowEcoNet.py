# Loading in Libraries
import requests
import os
import pandas as pd
import numpy as np
from ecoNet import*

## Job IDs:
# Moorea  
libraryID = '16616afa8edd490ea7e50cc316a20222'
analogID = '752f22be3e0746e1b0c4987acbc24d53'

# Moorea small nets
# libraryID = '5cbf1176ed26426fa9f8138681a883f7'
# analogID = '50cd02513cc0452589479d99ccc9333f'

# Pseudo-nitzchia
# libraryID = '89c9d8b0a49d467390b70dd337bc7015'
# analogID = '5c635e079c5a4eccbdcc7602eef88fc8'
# canopusID = '301eced29b3844e2b43ab6137871e216'

# Verification (no Lib ID's)
# libraryMatch = pd.read_csv('~/Documents/GitHub/ecoNet/verification/emptyLibrary.csv') 

# Get jobs
# N/A was added to the superclass. Filter for that
print('Getting GNPS jobs...')
libraryMatch = getJob(libraryID, 'library')
analogMatch = None
analogMatch = getJob(analogID, 'analog')  #change to if analog supplied
# canopusMatch = getJob(canopusID, 'canopus')
edgeInfo = getJob(libraryID, 'edges')

# Morea CANOPUS job and Network
canopusMatch = pd.read_csv('~/Documents/GitHub/DORCIERR/data/raw/metabolomics/sirius4_06012021/canopus_summary.csv') 
network = pd.read_csv('~/Documents/GitHub/DORCIERR/data/raw/metabolomics/Node_info.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})
# network = pd.read_csv('~/Documents/GitHub/ecoNet/verification/dorcierr_SmallNets/Node_info.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})

# PN network
# network = pd.read_csv('~/Downloads/pn_lib_cytoFile/clusterinfo_summary/524715591bc84b83b440eb32406c2610.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})[['scan', 'network']]

# Subset dataframes. Removed .df after libraryMatch if using verification data. 
librarySubset = libraryMatch.df[['#Scan#', 'superclass', 'class', 'subclass']]
librarySubset = librarySubset.replace('N/A', np.nan).add_suffix('_library').rename(columns={'#Scan#_library': 'scan'})

if analogMatch != None:
    weightAnalogs = True
    analogSubset = analogMatch.df[['#Scan#', 'superclass', 'class', 'subclass']]
    analogSubset = analogSubset.replace('N/A', np.nan).add_suffix('_analog').rename(columns={'#Scan#_analog': 'scan'})

if analogMatch == None:
    weightAnalogs = False
    analogSubset = False

canopusSubset = canopusMatch[['scan', 'superclass', 'class', 'subclass']].add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})
networkSubset = network[['scan', 'network']]

# Merge library, analogs and 
print(' ')
print('merging annotations...')
# network = makeNet(edgeInfo) # This is for once I figure out the edgeInfo table IF using this change network to network.networks below
merged = mergeAnnotations(librarySubset, canopusSubset, networkSubset, analog = analogSubset)

print(' ')
print('Weighting nodes by relative cosine score...')
weights = None
weights = weightEdges(edgeInfo) # Not all edges are in this dataframe.

# Printing to CL for user
print(' ')
print('finding consensus annotations...')
# Propogate annotations
if not weights == None:
    annotations = selectAnnotation(merged.library, merged.insilico, networkSubset, weights.edgeWeightings, analogWeight = weightAnalogs)

if weights == None:
    annotations = selectAnnotation(merged.library, merged.insilico, networkSubset, analogWeight = weightAnalogs, edgeWeights = None)

annotations.export.to_csv('ecoNetConsensus.csv')

# Caluculating %consensus
numLibrary = len(annotations.export[annotations.export['matchSource'] == 'Library'].dropna(subset = ['ecoNetConsensus'])[['network']].drop_duplicates())
totalLibrary = len(merged.library[merged.library['superclass_library'].notna() == True][['network']].drop_duplicates())
numInsilico = len(annotations.export[annotations.export['matchSource'] == 'Insilico'].dropna(subset = ['ecoNetConsensus'])[['network']].drop_duplicates())
totalInsicilo = len(merged.insilico[merged.insilico['superclass_canopus'].notna() == True][['network']].drop_duplicates())


libraryConsensus = round(numLibrary/totalLibrary, 4)
insilicoConsensus = round(numInsilico/totalInsicilo, 4)
totalConsensus = round(((numLibrary + numInsilico) / (totalInsicilo + totalLibrary)), 4)
# Reporting success rate for consensus sequences
print(' ')
print(str(str(numLibrary) + " out of " + str(totalLibrary) + " (" + str(libraryConsensus*100) + "%)" + " networks with Library ID's found a consensus annotation"))
print(str(str(numInsilico) + " out of "  + str(totalInsicilo) + " (" + str(insilicoConsensus*100) + "%)" +  " networks with Insilico annotations found a consensus annotation"))
print(str(str(totalConsensus*100) + "%" + " of all networks with an annotation recieved a consensus annotation"))





