# ConCISE Documentation
Welcome to the Documentation branch. To see the full documentation github pages go to zquinlan.github.io/conCISE/

### Concensus Classification from In Silico Elucidations 
[![DOI](https://zenodo.org/badge/366236409.svg)](https://zenodo.org/badge/latestdoi/366236409) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Zquinlan/conCISE/HEAD?labpath=src%2FconciseBinder.ipynb) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Zquinlan/conCISE/blob/master/LICENSE.txt) 
<br>
If you have any questions contact [Zach Quinlan](mailto:zquinlan@gmail.com).

# Contributing to the Documentation:
Feel free to help us maintain the documentation!

### Editing documentation
All documentation lives in _pages/ and can be editted in ``` .md ``` form.

### Makine new documents
Create a new ``` .md ``` file in _pages/. To the top of the page add:
```
---
layout: posts
    # classes: wide
sidebar:
    nav: "Documentation"
---
```
Then add this new documnent to the _data/navigation.yml with the title and url
```
- title: Gui Widgets
  url: /_pages/guiWidgets/index.html
```


# Citations:

*Dührkop, K., Fleischauer, M., Ludwig, M. et al. SIRIUS 4: a rapid tool for turning tandem mass spectra into metabolite structure information. Nat Methods 16, 299–302 (2019). https://doi.org/10.1038/s41592-019-0344-8

**Kai Dührkop, Louis-Félix Nothias, Markus Fleischauer, Raphael Reher, Marcus Ludwig, Martin A. Hoffmann, Daniel Petras, William H. Gerwick, Juho Rousu, Pieter C. Dorrestein and Sebastian Böcker. Systematic classification of unknown metabolites using high-resolution fragmentation mass spectra. Nature Biotechnology, 2020

***Wang, M., Carver, J., Phelan, V. et al. Sharing and community curation of mass spectrometry data with Global Natural Products Social Molecular Networking. Nat Biotechnol 34, 828–837 (2016). https://doi.org/10.1038/nbt.3597; Nothias, LF., Petras, D., Schmid, R. et al. Feature-based molecular networking in the GNPS analysis environment. Nat Methods 17, 905–908 (2020). https://doi.org/10.1038/s41592-020-0933-6
