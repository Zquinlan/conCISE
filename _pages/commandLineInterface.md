---
layout: posts
    # classes: wide
sidebar:
    nav: "Documentation"
---
# Command Line Interface and myBinder (conciseCLI.py, conciseBinder.ipynb)
This is the main workflow runner that all other methods will utilize. 

To use the CLI you will need to download the source code. The CLI code will run the workflow runner in the main workflow python file. To run the myBinder click the below icon which will boot the virtual machine. This process might take a bit as it is free. [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Zquinlan/conCISE/HEAD?labpath=src%2FconciseBinder.ipynb)

## Arguments:
- GNPS task ID
- Canopus_summary file
- Networking info file
- Superclass percent consensus (optional; default = 50)
- Class percent consensus (optional; default = 70)
- Subclass percent consensus (optional; default = 70)
- export directory for consensus file (optional; default = current working directory)

```Python
python3 src/conciseCLI.py 16616afa8edd490ea7e50cc316a20222 exampleFiles/canopus_summary.tsv exampleFiles/Node_info.tsv
```