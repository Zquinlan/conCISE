--- 
layout: posts 
classes: wide 
sidebar:
  nav: "content" 
---
```
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import argparse

#Arguments
parser = argparse.ArgumentParser()
parser.add_argument('infile', help = 'csv_dataframe')
parser.add_argument('sample_column', help = 'what is the name of the sample_column')
args = parser.parse_args()

#Reading in file
df = pd.read_csv(args.infile)

#Setting font and color pallette
current_palette = sns.color_palette("RdBu_r", 200)
#sns.set(font_scale = 0.3)

#set sample name and color
sample = df.pop(args.sample_column)


#Designing the plot
g = sns.clustermap(df, cmap = current_palette, metric = 'cityblock', 
    robust = True, yticklabels = sample, xticklabels = 1, figsize = (10,15))
plt.setp(g.ax_heatmap.xaxis.get_ticklabels(), fontsize = 3)
plt.setp(g.ax_heatmap.yaxis.get_ticklabels(), fontsize = 8)

#Showing the plot
plt.savefig('ClusterDenodgram.png', dpi = 600)

plt.show()```