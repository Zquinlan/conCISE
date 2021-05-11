import requests
import json
import pandas as pd

class getJob:
    def __init__(self, jobID, jobType):
        super().__init__()

        # Requesting tsv output from GNPS API
        self.id = jobID

        if jobType == 'canopus':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=canopus_summary') 
        if jobType == 'library':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=view_all_clusters_withID')
        if jobType == 'analog':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=view_all_analog_annotations_DB')

        # request JSON files from GNPS, clean and load into pandas
        self.request = requests.get(url) # Download JSON from GNPS
        self.clean = self.request.text.replace('{ "blockData" : [', '[').replace('] }', ']').strip()
        self.df = pd.read_json(self.clean)

class getInchiKeys:
    def __init__(self, inchis):
        super().__init__()

        self.inchiSeries = inchis
        # self.inchiSeries = self.inchis['INCHI'].to_list()

        host = "http://www.chemspider.com"
        getstring = "/InChI.asmx/InChIToInChIKey?inchi="


        self.inchikeys = []

        for i in self.inchiSeries:
            r = requests.get('{}{}{}'.format(host, getstring, i))
            if r.ok:
                res = str(r.text.replace('<?xml version="1.0" encoding="utf-8"?>\r\n<string xmlns="http://www.chemspider.com/">', '').replace('</string>', '').strip())
                self.inchikeys.append(res)
            else:
                self.inchikeys.append('NA')

        self.inchiFrame = self.inchiSeries.to_frame()
        self.inchiFrame['inchikey'] = self.inchikeys





