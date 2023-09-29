# Loading in Libraries
import os
import argparse
from workflowMain import *

# Arg parser setup
parser = argparse.ArgumentParser()
parser.add_argument('libraryID', help='GNPS library ID eg. 16616afa8edd490ea7e50cc316a20222')
parser.add_argument('canopusLocation', help='Unmidified canopus_summary.tsv file exported from SIRIUS4')
parser.add_argument('networkFile', help='network tsv file downloaded from GNPS')
parser.add_argument('superclassConsensus', nargs = '?', default = '50', help = 'Percent consensus for superclass (defaults to 50 percent and must be greater ≥ 50 percent)')
parser.add_argument('classConsensus', nargs = '?', default = '70', help = 'Percent consensus for class (defaults to 70 percent and must be greater ≥ 70 percent)')
parser.add_argument('subclassConsensus', nargs = '?', default = '70', help = 'Percent consensus for subclass (defaults to 70 percent and must be greater ≥ 70 percent)')
parser.add_argument('useNPClassifier', nargs = '?', default = False, help = 'Defaults to False and ConCISE will automatically use ClassyFire ontologies instead. If True, concise will use NPClassifier utilizing the superclass, class and Pathway columns')
parser.add_argument('exportDir', nargs = '?', default = 'None', help='What directory do you want to save the concise export file into?')
# parser.add_argument('analogID', help='Defaults to None. If you want it inlucded suuply the analog GNPS ID', default = 'None')
args = parser.parse_args()

if args.exportDir == 'None':
    export = os.getcwd()

if not args.exportDir == 'None':
    export = args.exportDir

wf = wfRunner()
wf.runWorkFlow(args.libraryID, args.canopusLocation, args.networkFile, export, args.superclassConsensus, args.classConsensus, args.subclassConsensus)