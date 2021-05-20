#Job IDs:
# canopus 301eced29b3844e2b43ab6137871e216
# library and analog
libraryID = '89c9d8b0a49d467390b70dd337bc7015'
analogID = '5c635e079c5a4eccbdcc7602eef88fc8'
canopusID = '301eced29b3844e2b43ab6137871e216'

# Loading in Libraries
# import argparse
import requests
import os
import csv 
import json
import pandas as pd
from ecoNet import*
# from pyMolNetEnhancer import*

# parser = argparse.ArgumentParser()
# parser.add_argument('task', help='GNPS Job ID')
# parser.add_argument('type', help='library, analog or canopus')
# args = parser.parse_args()

# Get jobs
# libraryMatch = getJob(libraryID, 'library')
# analogMatch = getJob(analogID, 'analog') 
# canopusMatch = getJob(canopusID, 'canopus')
# networkInfo = getJob(libraryID, network)

#Writing df for testing
# libraryMatch.df.to_csv('libraryTest.csv')
# analogMatch.df.to_csv('analogTest.csv')
# canopusMatch.df.to_csv('canopusTest.csv')

# For testing without having to request files
libraryMatch = pd.read_csv('libraryTest.csv')
analogMatch = pd.read_csv('analogTest.csv')
canopusMatch = pd.read_csv('canopusTest.csv') 
networkInfo = pd.read_csv('~/Downloads/pn_lib_cytoFile/clusterinfo_summary/524715591bc84b83b440eb32406c2610.tsv', sep='\t')


librarySubset = libraryMatch[['#Scan#', 'superclass', 'class', 'subclass']].add_suffix('_library').rename(columns={'#Scan#_library': 'scan'})
analogSubset = analogMatch[['#Scan#', 'superclass', 'class', 'subclass']].add_suffix('_analog').rename(columns={'#Scan#_analog': 'scan'})
canopusSubset = canopusMatch[['scan', 'superclass', 'class', 'subclass']].add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})
networkSubset = networkInfo[['cluster index', 'componentindex']].rename(columns={'cluster index': 'scan', 'componentindex': 'network'})

# Merge library, analogs and 
merged = mergeAnnotations(librarySubset, canopusSubset, networkSubset, analog = analogSubset)

# Propogate annotations
annotations = selectAnnotation(merged.library, merged.insilico, analogWeight = True)
