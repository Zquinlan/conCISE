---
layout: posts
    # classes: wide
sidebar:
    nav: "Documentation"
---
# Workflow
## Overview
This takes in the intial arguments and runs everything from concise in the correct order. 

## Steps:
### Reading tsv's
1. Converts whole percentages to decimal if needed.
2. Imports the canopus match information (works for both tsv and csv)
3. Renames the in silico columns as needed and captures both the most recent and previous versions of CANOPUS.

### Get requests
4. Gets the library (and analog) match datasets from GNPS
5. Gets edge info from GNPS for edgeWeighting

### merging annotations
6. Merging annotations with subnetwork information

### finding consensus annotations
7. Weights nodes if requested
8. Finds consensus annotations for every subnetwork at both library and in silico levels
9. Merges consensus annotations together, giving priority to library consensus annotatins
10. Reports success rates of consensus annotations