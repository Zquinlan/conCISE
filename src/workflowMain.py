# Loading in Libraries
import requests
import os
import pandas as pd
import numpy as np
import argparse
from math import ceil
from PyQt5.QtCore import QObject
from conCISE import*


class wfRunner(QObject):

    def __init__(self):
        super().__init__()
        temp = 0

    def runWorkFlow(self, libraryID, canopusLocation, networkFile, exportDirectory):
        ## Command line integration
        # libraryID = libraryID
        canopusMatch = pd.read_csv(canopusLocation, sep = '\t')
        canopusMatch['scan'] = canopusMatch['name'].str.split('_').str[-1].astype(int)

        network = pd.read_csv(networkFile, sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})


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

        try:
            canopusSubset = canopusMatch[['scan', 'superclass', 'class', 'subclass']].add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})
        except:
            canopusSubset = canopusMatch[['id', 'ClassyFire#superclass', 'ClassyFire#class', 'ClassyFire#subclass']].rename(columns = {'ClassyFire#superclass': 'superclass', 'ClassyFire#class': 'class', 'ClassyFire#subclass': 'subclass'}).add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})

        networkSubset = network[['scan', 'network']]

        # Merge library, analogs and 
        print(' ')
        print('merging annotations...')
        # network = makeNet(edgeInfo) # This is for once I figure out the edgeInfo table IF using this change network to network.networks below
        merged = mergeAnnotations(librarySubset, canopusSubset, networkSubset, analog = analogSubset)

        # print(' ')
        # print('Weighting nodes by relative cosine score...')
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

        exportDir = str(exportDirectory + '/conciseConsensus.csv')
        annotations.export.to_csv(exportDir)

        # Caluculating %consensus
        numLibrary = len(annotations.export[annotations.export['matchSource'] == 'Library'].dropna(subset = ['conciseConsensus'])[['network']].drop_duplicates())
        totalLibrary = len(merged.library[merged.library['superclass_library'].notna() == True][['network']].drop_duplicates())
        numInsilico = len(annotations.export[annotations.export['matchSource'] == 'In silico'].dropna(subset = ['conciseConsensus'])[['network']].drop_duplicates())
        totalInsicilo = len(merged.insilico[merged.insilico['superclass_canopus'].notna() == True][['network']].drop_duplicates())


        libraryConsensus = ceil(numLibrary/totalLibrary *100**2)/100**2
        insilicoConsensus = ceil(numInsilico/totalInsicilo*100**2)/100**2
        totalConsensus = ceil(((numLibrary + numInsilico) / (totalInsicilo + totalLibrary))*100**2)/100**2
        # Reporting success rate for consensus sequences
        print(' ')
        print(str(str(numLibrary) + " out of " + str(totalLibrary) + " (" + str(libraryConsensus*100) + "%)" + " networks with Library ID's found a consensus annotation"))
        print(str(str(numInsilico) + " out of "  + str(totalInsicilo) + " (" + str(insilicoConsensus*100) + "%)" +  " networks with Insilico annotations found a consensus annotation"))
        print(str(str(totalConsensus*100) + "%" + " of all networks with an annotation recieved a consensus annotation"))
        print(' ')
        print(str('conciseConsensus csv summary exported to: ' + exportDirectory))

        #Sending to Gui
        # terminalStr(str(str(numLibrary) + " out of " + str(totalLibrary) + " (" + str(libraryConsensus*100) + "%)" + " networks with Library ID's found a consensus annotation"))
        # terminalStr(str(str(numInsilico) + " out of "  + str(totalInsicilo) + " (" + str(insilicoConsensus*100) + "%)" +  " networks with Insilico annotations found a consensus annotation"))
        # terminalStr(str(str(totalConsensus*100) + "%" + " of all networks with an annotation recieved a consensus annotation"))
        # terminalStr(str('conciseConsensus csv summary exported to:' + exportDirectory))



