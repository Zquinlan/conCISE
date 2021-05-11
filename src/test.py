import numpy as np
# import json
# import pandas as pd
# from pyMolNetEnhancer import *
from ecoNet import *

job = '89c9d8b0a49d467390b70dd337bc7015'


# Requesting tsv output from GNPS API
test = getJob(job, 'edges')

weighted = weightEdges(test)

# test.df.to_csv('err/networkTest.csv')