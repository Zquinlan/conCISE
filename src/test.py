import json
import pandas as pd
from pyMolNetEnhancer import *
from ecoNet import *
libraryID = '83eff73ee6354c2da585ec5116d943aa'
analogID = '0b7329c9409b4d2381e63599a0f77038'

analogMatch = getJob(analogID, 'analog') 
libraryMatch = getJob(libraryID, 'library')

analogMatch.df.to_csv('analogTest.csv')
libraryMatch.df.to_csv('libraryTest.csv')