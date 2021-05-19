import requests
import json
import pandas as pd
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

        self.library = network.merge(library, on = 'scan', how = 'right')

        #Joining supplied dataframes
        if isinstance(analog, pd.DataFrame):
            self.matches = network.merge(analog, on = 'scan', how = 'outer')
            self.matches = self.matches.merge(canopus, on = 'scan', how = 'outer')   
            self.grouped = self.matches.groupby('network').apply(lambda x: x.dropna(subset = ['superclass_analog', 'superclass_canopus'], how = 'all'))

        if not isinstance(analog, pd.DataFrame):
            self.matches = network.merge(canopus, on = 'scan', how = 'outer')
            self.grouped = self.matches.groupby('network').apply(lambda x: x.dropna(ubset = ['superclass_canopus']))

        # Make a list of networks which have at least one Library Match and remove them from the analog/canopus annotaitons
        self.libraryNetworks = self.library['network'].drop_duplicates().tolist()
        self.insilico = self.grouped[self.grouped['network'].apply(lambda x: x not in self.libraryNetworks)]

        # self.insilico.reset_index(drop = True).to_csv('testView.csv')

class weightNodes:
    def __init__(self, library, insilico, libraryWeight = True, analogWeight = True):
        """
        library: The library file merged with network information exported from mergeAnnotations.library
        insilico: The canopus and analog classyfire information merged with network information exported from mergeAnnotations.insilico.

        All inputs need to be the direct output of mergeAnnotations()

        This function will return...
        """
        super().__init__()

        if libraryWeight == True:
            if analogWeight == True:
                
            if analogWeight != True:

        if libraryWeight != True:



