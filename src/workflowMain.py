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

    def runWorkFlow(self, libraryID, canopusLocation, networkFile, exportDirectory, superclassConsensus, classConsensus, subclassConsensus, useNP):
        ## Command line integration
        # libraryID = libraryID
        if float(superclassConsensus) > 1:
            superclassConsensus = float(superclassConsensus)/100
        if float(classConsensus) > 1:
            classConsensus = float(classConsensus)/100
        if float(subclassConsensus) > 1:
            subclassConsensus = float(subclassConsensus)/100
        

        try:
            canopusMatch = pd.read_csv(canopusLocation, sep = '\t')
        except: 
            canopusMatch = pd.read_csv(canopusLocation)

        # try:
        #     canopusMatch.rename(columns={'scan': 'featureNumber'})
        if 'mappingFeatureId' in canopusMatch.columns:
            canopusMatch['scan'] = canopusMatch['mappingFeatureId']
        elif 'name' in canopusMatch.columns:
            canopusMatch['scan'] = canopusMatch['name'].str.split('_').str[-1].astype(int)
        elif 'id' in canopusMatch.columns:
            canopusMatch['scan'] = canopusMatch['id'].str.split('_').str[-1].astype(int)
            
        try:
            networkRaw = pd.read_csv(networkFile, sep = '\t')
        except:
            networkRaw = pd.read_csv(networkFile)

        try:
            network = networkRaw.rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})
            networkSubset = network[['scan', 'network']]
        except:
            network = networkRaw.rename(columns = {'cluster index': 'scan', 'component': 'network'})
            networkSubset = network[['scan', 'network']]


        # Get jobs
        # N/A was added to the superclass. Filter for that
        print('Getting GNPS jobs...')

        # Read in the library file. This will either read in a csv/tsv or get the library job from GNPS
        if ".csv" in libraryID or ".tsv" in libraryID:
            try:
                libraryMatch = pd.read_csv(libraryID)
            except:
                libraryMatch = pd.read_csv(libraryID, sep = '\t')

            libraryDataFrame = libraryMatch

        else:
            libraryMatch = getJob(libraryID, 'library')
            libraryDataFrame = libraryMatch.df
            
        # libraryMatch = pd.read_csv('~/Downloads/rrCoral/libraryMatchesFixed.csv') # If this line is uncommented it allows me to upload a version of the library match file manually
        analogMatch = None

        # edgeInfo = getJob(libraryID, 'edges')

        # Subset dataframes. Removed .df after libraryMatch if using verification data. 
        # Check if using NPC for library matches
        if useNP == False:
            librarySubset = libraryDataFrame[['#Scan#', 'superclass', 'class', 'subclass']]
        else:
            librarySubset = libraryDataFrame[['#Scan#', 'npclassifier_pathway', 'npclassifier_superclass', 'npclassifier_class']].rename(columns={'npclassifier_pathway' : 'superclass', 'npclassifier_superclass': 'class', 'npclassifier_class': 'subclass'})
            

        librarySubset = librarySubset.replace('N/A', np.nan).add_suffix('_library').rename(columns={'#Scan#_library': 'scan'})

        # Check if using analog matches
        if analogMatch != None:
            weightAnalogs = True
            analogSubset = analogMatch.df[['#Scan#', 'superclass', 'class', 'subclass']]
            analogSubset = analogSubset.replace('N/A', np.nan).add_suffix('_analog').rename(columns={'#Scan#_analog': 'scan'})
        else:
            weightAnalogs = False
            analogSubset = False

        #Check if using NPC for in silico matches
        if useNP == False:
            try:
                canopusSubset = canopusMatch[['scan', 'superclass', 'class', 'subclass']].add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})
            except:
                canopusSubset = canopusMatch[['scan', 'ClassyFire#superclass', 'ClassyFire#class', 'ClassyFire#subclass']].rename(columns = {'ClassyFire#superclass': 'superclass', 'ClassyFire#class': 'class', 'ClassyFire#subclass': 'subclass'}).add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})
        else:
            canopusSubset = canopusMatch[['scan', 'NPC#pathway', 'NPC#superclass', 'NPC#class']].rename(columns = {'NPC#pathway': 'superclass', 'NPC#superclass': 'class', 'NPC#class': 'subclass'}).add_suffix('_canopus').rename(columns={'scan_canopus': 'scan'})

        

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
            annotations = selectAnnotation(merged.library, merged.insilico, networkSubset, weights.edgeWeightings, analogWeight = weightAnalogs, superclassMinimum = float(superclassConsensus), classMinimum = float(classConsensus), subclassMinimum = float(subclassConsensus))
        else:
            annotations = selectAnnotation(merged.library, merged.insilico, networkSubset, analogWeight = weightAnalogs, edgeWeights = None, superclassMinimum = float(superclassConsensus), classMinimum = float(classConsensus), subclassMinimum = float(subclassConsensus))

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
        print(str(str(totalConsensus*100) + "%" + " of all networks with an annotation received a consensus annotation"))
        print(' ')
        print(str('conciseConsensus csv summary exported to: ' + exportDirectory))

        #Sending to Gui
        # terminalStr(str(str(numLibrary) + " out of " + str(totalLibrary) + " (" + str(libraryConsensus*100) + "%)" + " networks with Library ID's found a consensus annotation"))
        # terminalStr(str(str(numInsilico) + " out of "  + str(totalInsicilo) + " (" + str(insilicoConsensus*100) + "%)" +  " networks with Insilico annotations found a consensus annotation"))
        # terminalStr(str(str(totalConsensus*100) + "%" + " of all networks with an annotation recieved a consensus annotation"))
        # terminalStr(str('conciseConsensus csv summary exported to:' + exportDirectory))



