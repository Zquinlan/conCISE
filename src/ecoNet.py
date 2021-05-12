import requests
import json
import pandas as pd
import csv
from pyMolNetEnhancer import *

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
    def __init__(self, smiles):
        super().__init__()

        self.smilesSeries = smiles
        self.inchikeys = []

        for i in self.smilesSeries:
            r = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{i}/property/inchikey/JSON")
            try:
                res = r.json()
                inchikey = res['PropertyTable']['Properties'][0]['InChIKey']
                self.inchikeys.append(inchikey)
            except KeyError:
                self.inchikeys.append('NA')
            except json.decoder.JSONDecodeError:
                self.inchikeys.append('NA')

        self.inchiFrame = self.smilesSeries.to_frame()
        self.inchiFrame['InChIKey'] = self.inchikeys

#get_classifications from MolNetEnhancer without strip('=')
def get_classifier(inchifile):

    with open(inchifile) as csvfile:
        all_inchi_keys = []
    
        reader = csv.DictReader(csvfile)
        row_count = 0
        for row in reader:
            row_count += 1
    
            if row_count % 1000 == 0:
                print(row_count)
    
            all_inchi_keys.append(row["InChIKey"])
    
            continue
    
        #all_inchi_keys = all_inchi_keys[-1000:]
        all_json = run_parallel_job(get_structure_class_entity, all_inchi_keys, parallelism_level = 50)
    
        open("all_json.json", "w").write(json.dumps(all_json))



