import requests
import argparse
import json
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('task', help='GNPS Job ID')
parser.add_argument('type', help='library or nap')
args = parser.parse_args()

class getJob:
    def __init__(self, jobID, jobType):
        super().__init__()

        # Requesting tsv output from GNPS API
        self.id = jobID

        if jobType == 'nap':
            url = str('http://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task=' + self.id + '&block=main&file=final_out/node_attributes_table.tsv') 
            self.df = pd.read_csv(url, sep = '\t') # Download tsv from GNPS
        if jobType == 'library':
            url = str('https://gnps.ucsd.edu/ProteoSAFe/result_json.jsp?task=' + self.id + '&view=view_all_clusters_withID')
            self.df = pd.read_json(url)

        print(self.df)

         

        # with open('test_nap.json', 'w') as f:
        #     json.dump(self.json, f)

getJob(args.task, args.type)

#nap = ef8f40d00aa94e9b91aad6b00258ffc6
#gnps = d7373e2add2a4e72a871a60c96fbbbc3
