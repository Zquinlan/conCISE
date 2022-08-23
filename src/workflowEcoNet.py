# Loading in Libraries
import requests
import os
import pandas as pd
import numpy as np
import argparse
from ecoNet import*

# Arg parser setup
parser = argparse.ArgumentParser()
parser.add_argument('libraryID', help='GNPS library ID eg. 16616afa8edd490ea7e50cc316a20222')
parser.add_argument('canopusLocation', help='Unmidified canopus_summary.tsv file exported from SIRIUS4')
parser.add_argument('networkFile', help='network tsv file downloaded from GNPS')
# parser.add_argument('analogID', help='Defaults to None. If you want it inlucded suuply the analog GNPS ID', default = 'None')
args = parser.parse_args()

## Command line integration
libraryID = args.libraryID

canopusMatch = pd.read_csv(args.canopusLocation, sep = '\t')
canopusMatch['scan'] = canopusMatch['name'].str.split('_').str[-1].astype(int)

network = pd.read_csv(args.networkFile, sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})
# analogMatch = args.analogId


# Get jobs
# N/A was added to the superclass. Filter for that
print('Getting GNPS jobs...')
libraryMatch = getJob(libraryID, 'library')
analogMatch = None
# analogMatch = getJob(analogID, 'analog')  #change to if analog supplied
# canopusMatch = getJob(canopusID, 'canopus')
edgeInfo = getJob(libraryID, 'edges')

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
# weights = weightEdges(edgeInfo) # Not all edges are in this dataframe.

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
numInsilico = len(annotations.export[annotations.export['matchSource'] == 'In silico'].dropna(subset = ['ecoNetConsensus'])[['network']].drop_duplicates())
totalInsicilo = len(merged.insilico[merged.insilico['superclass_canopus'].notna() == True][['network']].drop_duplicates())


libraryConsensus = round(numLibrary/totalLibrary, 4)
insilicoConsensus = round(numInsilico/totalInsicilo, 4)
totalConsensus = round(((numLibrary + numInsilico) / (totalInsicilo + totalLibrary)), 4)
# Reporting success rate for consensus sequences
print(' ')
print(str(str(numLibrary) + " out of " + str(totalLibrary) + " (" + str(libraryConsensus*100) + "%)" + " networks with Library ID's found a consensus annotation"))
print(str(str(numInsilico) + " out of "  + str(totalInsicilo) + " (" + str(insilicoConsensus*100) + "%)" +  " networks with Insilico annotations found a consensus annotation"))
print(str(str(totalConsensus*100) + "%" + " of all networks with an annotation recieved a consensus annotation"))





