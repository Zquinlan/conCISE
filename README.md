# ConCISE 
### Concensus Classification from In Silico Elucidations 
[![DOI](https://zenodo.org/badge/366236409.svg)](https://zenodo.org/badge/latestdoi/366236409) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Zquinlan/conCISE/HEAD?labpath=src%2FconciseBinder.ipynb) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Zquinlan/conCISE/blob/master/LICENSE.txt) 
<br>
<br>
### New feature requests? 
I am actively working on a larger update to ConCISE and am definitely interested in hearing what updates the community would like added. Raise an issue requesting it or send me an email and I will add it to my list.
<br>
### ***Known issue and workaround*** 
Currently GNPS has stopped supplying classyfire ontology information for spectral library matches. There are two workarounds: 1) use NPClassifier instead of ClassyFire by checking the box in the GUI or changing the NPC argument from False to True. 2) Manually pull classyfire data for your library match data. You can copy the InChiKey's from the GNPS DBResult file into the Fiehn Labs' [classyfire Batch](https://cfb.fiehnlab.ucdavis.edu/) identifier. Once these results are merged back into the original GNPS DBResult file with the correct column names (i.e. superclass, class, subclass), you can use this file in place of the libraryID.
<br>
<br>
<br>
#### ConCISE utlizes the structural annotations provided by in silico tools such as [SIRIUS](https://bio.informatik.uni-jena.de/software/)* and CANOPUS** combined with networking tools from [GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp) such as feature based molecular networking***.

You can run this tool locally using the graphical user interface and command line interface, or on a virtual machine using the above binder link.

ConCISE works by finding consensus annotations of putative annotations using the ClassyFire ontologies which are supplied by GNPS for library spectral matches and in silico putative annotations. 

If you have any questions contact [Zach Quinlan](mailto:zquinlan@gmail.com).

If you have problems runnning conCISE please open an issue with your error and input files and I will help ASAP. :)


# Download links:
### Graphical user interface
- [Windows](https://github.com/Zquinlan/conCISE/releases/download/v1.30/conCISEGui.exe)
- [Mac] -- Currently the GUI for Mac is deprecated. To currently use ConCISE onMac, please use the command line or MyBinder interfaces. Once I get a Apple Developer Xcode number, I will recreate the GUI for mac.

### Command line interface
To use the CLI you will need to [download](https://github.com/zquinlan/concise/releases) the source code. The CLI code will run the workflow runner in the main workflow python file.

#### Arguments:
- GNPS task ID or spectral library match file
- Canopus_summary file
- Networking info file
- export directory for consensus file (optional; default = current working directory)
- Superclass percent consensus (optional; default = 50)
- Class percent consensus (optional; default = 70)
- Subclass percent consensus (optional; default = 70)
- Use NPClassifier in place of ClassyFire Ontologies (True or False; e.g., 'True' will utilize NPClassifier ontologies for both library matches and in silico matches)

```Python
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv 50 70 70 False
```

### Virtual machine run through myBinder
myBinder offers a free virtual machine to run the jupyter notebook.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Zquinlan/conCISE/HEAD?labpath=src%2FconciseBinder.ipynb)


### [Version History](https://github.com/zquinlan/concise/releases)

# Documentation:
Documentation is available [here](https://zquinlan.github.io/conCISE/).

# Issues:
#### Help us improve ConCISE

- For bug reports or feature requests please open an "issue" on [this github repository](https://github.com/Zquinlan/conCISE/issues) 
- If you would like to contribute to the development of ConCISE for other applications fork this repository and make a pull request with your changes. Or reach out directly to us to see if these changes are already being implemented in beta updates.

# Citations:

*Dührkop, K., Fleischauer, M., Ludwig, M. et al. SIRIUS 4: a rapid tool for turning tandem mass spectra into metabolite structure information. Nat Methods 16, 299–302 (2019). https://doi.org/10.1038/s41592-019-0344-8

**Kai Dührkop, Louis-Félix Nothias, Markus Fleischauer, Raphael Reher, Marcus Ludwig, Martin A. Hoffmann, Daniel Petras, William H. Gerwick, Juho Rousu, Pieter C. Dorrestein and Sebastian Böcker. Systematic classification of unknown metabolites using high-resolution fragmentation mass spectra. Nature Biotechnology, 2020

***Wang, M., Carver, J., Phelan, V. et al. Sharing and community curation of mass spectrometry data with Global Natural Products Social Molecular Networking. Nat Biotechnol 34, 828–837 (2016). https://doi.org/10.1038/nbt.3597; Nothias, LF., Petras, D., Schmid, R. et al. Feature-based molecular networking in the GNPS analysis environment. Nat Methods 17, 905–908 (2020). https://doi.org/10.1038/s41592-020-0933-6
