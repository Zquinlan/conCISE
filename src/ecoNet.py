import requests
import json
import pandas as pd
import numpy as np
import csv
from pyMolNetEnhancer import *

class getJob:
    def __init__(self, jobID, jobType):
        super().__init__()
        """
        jobID: This is the task number of your GNPS job which can be found in the url of your GNPS job
        jobType: The type of job options are 'canopus', 'library', 'analog', 'network'
        
        All of these jos are needed to run the rest of the pipeline. Analogs are optional and do not to be downloaded.
        """

        # Requesting tsv output from GNPS API
        self.id = jobID

        if jobType == 'canopus':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=canopus_summary') 
        if jobType == 'library':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=view_all_annotations_DB')
        if jobType == 'analog':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=view_all_analog_annotations_DB')
        if jobType == 'network':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=view_all_analog_annotations_DB')

        # request JSON files from GNPS, clean and load into pandas
        self.request = requests.get(url) # Download JSON from GNPS
        self.clean = self.request.text.replace('{ "blockData" : [', '[').replace('] }', ']').strip()
        self.df = pd.read_json(self.clean)

class mergeAnnotations:
    def __init__(self, library, canopus, network, analog = None):
        """
        library: The library match file downloaded from GNPS
        canopus: The Canopus file which can be downloaded from the SIRIUS workflow
        network: The Network file which is found in the clusterInfoSummary directory downloaded from GNPS
        analog: (Optional) The Analog file which can be downloaded from GNPS.

        All inputs need to be pd.DataFrames and not modified from how GNPS exports them.
        The dataframes can be directly downloaded using getJob() with the correct jobType specified.

        This function will return self.library and self.insilico which will have the library and insilico merged files for use in weighting and annotation propogation.
        """
        super().__init__()

        self.library = network.merge(library, on = 'scan', how = 'right').dropna(subset = ['superclass_library'])

        #Joining supplied dataframes
        if isinstance(analog, pd.DataFrame):
            self.matches = network.merge(analog, on = 'scan', how = 'outer')
            self.matches = self.matches.merge(canopus, on = 'scan', how = 'outer')   
            self.grouped = self.matches.groupby('network').apply(lambda x: x.dropna(subset = ['superclass_analog', 'superclass_canopus'], how = 'all'))

        if not isinstance(analog, pd.DataFrame):
            self.matches = network.merge(canopus, on = 'scan', how = 'outer')
            self.grouped = self.matches.groupby('network').apply(lambda x: x.dropna(subset = ['superclass_canopus']))

        # Make a list of networks which have at least one Library Match and remove them from the analog/canopus annotaitons
        self.libraryNetworks = self.library['network'].drop_duplicates().tolist()
        self.insilico = self.grouped[self.grouped['network'].apply(lambda x: x not in self.libraryNetworks)]

        # self.insilico.reset_index(drop = True).to_csv('testView.csv')

class selectAnnotation:
    def __init__(self, library, insilico, analogWeight = True, absoluteMinimum = 0.5, classMinimum = 0.7): # Add absoluteMinimum , etc as argument
        """
        library: The library file merged with network information exported from mergeAnnotations.library
        insilico: The canopus and analog classyfire information merged with network information exported from mergeAnnotations.insilico.
        absoluteMinimum: Minimum consensus score for superclass consensus (Defaults to >50%)
        classMinimum: Minimum consensus score for class and subclass (Defaults to >= 70%) 

        library and insilico inputs need to be the direct output of mergeAnnotations()

        This returns a dataframe which has libraryAnnotations and Insilico annotations for every network which meets 
        """
        super().__init__()

        def selectClassy(df, returnType): #This needs to change to %like% as well as filterClassy
            subclassCol = df.index.values[(df.index.str.startswith('subclass') == True) & (df.index.str.endswith('ion') == False)]
            classCol = df.index[(df.index.str.startswith('class') == True) & (df.index.str.endswith('ion') == False)]
            superclassCol = df.index[(df.index.str.startswith('superclass') == True) & (df.index.str.endswith('ion') == False)]
            
            subclassCol = str(subclassCol).split("['")[1]
            subclassCol = str(subclassCol).split("']")[0]

            classCol = str(classCol).split("['")[1]
            classCol = str(classCol).split("']")[0]
            
            superclassCol = str(superclassCol).split("['")[1]
            superclassCol = str(superclassCol).split("']")[0]


            if (df[subclassCol] >= 0.7) & (df[classCol] >= 0.7) & (df[superclassCol] > 0.5):
                if returnType == 'annotation':
                    return df['subclass_annotation']
                if returnType == 'score':
                    return df[subclassCol]
 
            elif (df[classCol] >= 0.7) & (df[superclassCol] > 0.5):
                if returnType == 'annotation':
                    return df['class_annotation']
                if returnType == 'score':
                    return df[classCol]

            elif (df[superclassCol] > 0.5):
                if returnType == 'annotation':
                    return df['superclass_annotation']
                if returnType == 'score':
                    return df[superclassCol]

        def selectInsilico(insilico, taxLevel, analogWeight):
            canopusCol = str(taxLevel + '_canopus')
            analogCol = str(taxLevel + '_analog')

            if analogWeight == True:
                    if (pd.isnull(insilico['superclass_analog']) == True) & (pd.isnull(insilico['superclass_canopus']) == False):
                        return insilico[canopusCol]
                    elif (pd.isnull(insilico['superclass_analog']) == False) & (pd.isnull(insilico['superclass_canopus']) == True):
                        return  insilico[analogCol]
                    elif (pd.isnull(insilico['superclass_analog']) == False) & (pd.isnull(insilico['superclass_canopus']) == False):
                        return  insilico[analogCol]

            # if asnalogWeight == False:


        def filterClassy(groupedData, matchType, absoluteMinimum, classMinimum):
            """
            groupedData: data grouped by network (or featNets)
            matchType: Either library or insilico Matches
            absoluteMinimum: Minimum consensus score for superclass consensus (Defaults to >50%)
            classMinimum: Minimum consensus score for class and subclass (Defaults to >= 70%) 

            """
            if matchType == 'library':
                superclassStr = 'superclass_library'
                classStr = 'class_library'
                subclassStr = 'subclass_library'
                mergeOn = 'featNets'

            if matchType == 'insilico':
                superclassStr = 'superclass_insilico'
                classStr = 'class_insilico'
                subclassStr = 'subclass_insilico'
                mergeOn = 'network'

            superclassTop = groupedData[superclassStr].apply(lambda x: x.value_counts(normalize = True)).reset_index()
            superclassFiltered = superclassTop[superclassTop[superclassStr] > absoluteMinimum].rename(columns={'level_1': 'superclass_annotation'})

            classTop = groupedData[classStr].apply(lambda x: x.value_counts(normalize = True)).reset_index()
            classFiltered = classTop[classTop[classStr] > classMinimum].rename(columns={'level_1': 'class_annotation'})

            subclassDf = groupedData[subclassStr].apply(lambda x: x.value_counts(normalize = True)).reset_index()
            subclassFiltered = subclassDf[subclassDf[subclassStr] > classMinimum].rename(columns={'level_1': 'subclass_annotation'})

            # Merge ontologies and drop NA's
            merged = superclassFiltered.merge(classFiltered, on = mergeOn, how = 'outer').merge(subclassFiltered, on = mergeOn, how = 'outer')
            mergedFiltered = merged.dropna(subset = ['superclass_annotation', 'class_annotation', 'subclass_annotation'], how = 'all')
            mergedFiltered['ecoNetConsensus'] = mergedFiltered.apply(lambda x: selectClassy(x, 'annotation'), axis = 1)
            mergedFiltered['ecoNetConsensusScore'] = mergedFiltered.apply(lambda x: selectClassy(x, 'score'), axis = 1)

            return mergedFiltered

        # Need a networks column which has feature numbers for single loop nodes
        library.loc[library['network'] == '-1', 'featNets'] = library['scan']*-1
        library.loc[library['network'] != '-1', 'featNets'] = library['network']

        # Grouping by network
        self.library = library.groupby('featNets')

        # Making library Filtered ClassyStrings result
        self.libraryFiltered = filterClassy(self.library, 'library', absoluteMinimum, classMinimum) #absoluteMinimum and classMinimum are defined in the main function
        self.libraryFiltered.to_csv('err/LibraryClassifcationPropogation.csv')

        for col in ['superclass', 'class', 'subclass']:
            newCol = str(col + '_insilico')
            insilico[newCol] = insilico.apply(lambda x: selectInsilico(x, col, analogWeight), axis = 1)

        insilicoCombined = insilico[['scan', 'network', 'superclass_insilico', 'class_insilico', 'subclass_insilico']].reset_index(drop = True) 
        insilicoCombinedGrouped = insilicoCombined.groupby('network')

        self.insilicoFiltered = filterClassy(insilicoCombinedGrouped, 'insilico', absoluteMinimum, classMinimum) #absoluteMinimum and classMinimum are defined in the main function
        self.insilicoFiltered.to_csv('err/InsilicoClassificationPropogation.csv')

        # if libraryWeight != True:



