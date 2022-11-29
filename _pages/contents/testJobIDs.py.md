--- 
layout: posts 
classes: wide 
sidebar:
  nav: "content" 
---
```
# Here are the ID's for all the different test dataframes 
# as well as locations for all the various files


## Job IDs:
# Moorea  
# libraryID = '16616afa8edd490ea7e50cc316a20222'
# analogID = '752f22be3e0746e1b0c4987acbc24d53'

# Moorea small nets
# libraryID = '5cbf1176ed26426fa9f8138681a883f7'
# analogID = '50cd02513cc0452589479d99ccc9333f'

# Pseudo-nitzchia
# libraryID = '89c9d8b0a49d467390b70dd337bc7015'
# analogID = '5c635e079c5a4eccbdcc7602eef88fc8'
# canopusID = '301eced29b3844e2b43ab6137871e216'

# Aron
# libraryID = 'a94feb20e4214375bf89dfbe2b28fbd4'

# diel prelim
# libraryID = '4d63e1adb2534d4c9901f2e64d3cbec2'

# Coral 3D
# libraryID = ''
# analogID = ''

# Verification (no Lib ID's)
# libraryMatch = pd.read_csv('~/Documents/GitHub/ecoNet/verification/emptyLibrary.csv') 



# Moorea CANOPUS job and Network
# canopusMatch = pd.read_csv('~/Documents/GitHub/DORCIERR/data/raw/metabolomics/sirius4_06012021/canopus_summary.csv') 
# network = pd.read_csv('~/Documents/GitHub/DORCIERR/data/raw/metabolomics/Node_info.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})
# network = pd.read_csv('~/Documents/GitHub/ecoNet/verification/dataset1_SmallNets/Node_info.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})

# PN network
# network = pd.read_csv('~/Downloads/pn_lib_cytoFile/clusterinfo_summary/524715591bc84b83b440eb32406c2610.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})[['scan', 'network']]

# coral 3D
# canopusMatch = pd.read_csv('~/Documents/GitHub/ecoNet/verification/dataset3_unmodified/canopus_summary.csv') 
# network = pd.read_csv('~/Documents/GitHub/ecoNet/verification/dataset3_unmodified/Node_info.tsv', sep = '\t') .rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})[['scan', 'network']]

# aron
# canopusMatch = pd.read_csv('~/Documents/SDSU_Scripps/aron/canopus_aron.csv')
# network = pd.read_csv('~/Documents/SDSU_Scripps/aron/network_aron.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})[['scan', 'network']]

# diel prelim
# canopusMatch = pd.read_csv('~/Documents/SDSU_Scripps/Diel_prelim2019/canopus_summary.csv')
# network = pd.read_csv('~/Documents/SDSU_Scripps/Diel_prelim2019/node_info.tsv', sep = '\t').rename(columns = {'cluster index': 'scan', 'componentindex': 'network'})[['scan', 'network']]
```