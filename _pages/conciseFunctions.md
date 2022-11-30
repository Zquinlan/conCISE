# conCISE functions (conCISE.py)
## Classes:
- getJob
- mergeAnnotations
- weightEdges
- makeNet
- selectAnnotation

## getJob
This will utilize the GNPS API to pull either the GNPS library matches or GNPS analog matches. When more functionality is added to the GNPS API this will be incorporated into conCISE to pull all needed dataframes and not just library matches.

#### Arguments:
- jobID: This is the task number of your GNPS job which can be found in the url of your GNPS job
- jobType: The type of job options are 'canopus', 'library', 'analog', 'csiFingerID', 'edges' canopus, library and edges are all files which are needed to run the ConCISE pipeline)

## mergeAnnotations
Merge annotations combines the library or in silico annotations with network number and creates a new column and prepares the data for weighting or annotation selection.

#### Arguments:
- library: The library match file downloaded from GNPS
- canopus: The Canopus file which can be downloaded from the SIRIUS workflow
- network: The Network file which is found in the clusterInfoSummary directory downloaded from GNPS
- analog: (Optional) The Analog file which can be downloaded from GNPS.

All inputs need to be pd.DataFrames and not modified from how GNPS exports them.
The dataframes can be directly downloaded using getJob() with the correct jobType specified. 
This function will return self.library and self.insilico which will have the library and insilico merged files for use in weighting and annotation propogation.

## weightEdges
Currently this function is not in use and is a place holder for edge weighting to be incorporated into ConCISE.

## makeNet
This 

## selectAnnotation
his returns a dataframe which has libraryAnnotations and Insilico annotations for every network which meets the thresholds specified. Within this class it will go through each ion feature to find the lowest chemont level. It has functionality already written in selectInsilico to overwrite in silico annotations with analog annotations. This can and will be changed in future versions to utilize analog annotations in a different function. Finally filterClassy will combine library consenus, in silico consensus annotations and edge weighting (once incorporated).

#### Arguments:
- library: The library file merged with network information exported from mergeAnnotations.library
- insilico: The canopus and analog classyfire information merged with network information exported from mergeAnnotations.insilico.
- network: Full network and nodes for adding annotations
- superclassMinimum: Minimum consensus score for superclass consensus (Defaults to >50%)
- classMinimum: Minimum consensus score for class (Defaults to >= 70%)
- subclassMinimum: Minimum consensus score for subclass (Defaults to >= 70%) 
- library and insilico inputs need to be the direct output of mergeAnnotations()  