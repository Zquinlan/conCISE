# Loading in Libraries
import os
import argparse
from wfRunner import wfRunner
from workflowMain import *

# Arg parser setup
parser = argparse.ArgumentParser()
parser.add_argument('libraryID', help='GNPS library ID eg. 16616afa8edd490ea7e50cc316a20222')
parser.add_argument('canopusLocation', help='Unmidified canopus_summary.tsv file exported from SIRIUS4')
parser.add_argument('networkFile', help='network tsv file downloaded from GNPS')
parser.add_argument('exportDir', nargs = '?', default = 'None', help='What directory do you want to save the concise export file into?')
# parser.add_argument('analogID', help='Defaults to None. If you want it inlucded suuply the analog GNPS ID', default = 'None')
args = parser.parse_args()

if args.exportDir == 'None':
    export = os.getcwd()

if not args.exportDir == 'None':
    export = args.exportDir

wf = wfRunner()
wf.runWorkFlow(args.libraryID, args.canopusLocation, args.networkFile, export)