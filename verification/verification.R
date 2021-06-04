# Verification of Eco Net consesnsus scores
# Load Libraries
library(tidyverse)
library(DescTools)

select <- dplyr::select

# Reading in all data which could be gathered from respecrtive datasets
# set all locations:
path1 <- 'dorcierr'
path2 <- 'dorcierrNAP'
path3 <- 'dorcierrSmallNets'
path4 <- 'psuedonitzchia'
paths <- c(path1, path2, path3, path4)

# Combine all verification datasets
for (name in paths){
  
  path <- paste0('~/Documents/GitHub/ecoNet/verification/', name)
    
  network <- read_tsv(paste0(path, '/Node_info.tsv'))%>%
    select(`cluster index`, componentindex)%>%
    rename(feature_number = 1,
           network = 2)
  
  libraryMatches <- read_csv(paste0(path, "/libraryMatch.csv"))%>%
    rename("feature_number" = '#Scan#',
           library_superclass = superclass, 
           library_class = class, 
           library_subclass = subclass)%>%
    select(feature_number, library_superclass, library_class, library_subclass)
  
  analogMatches <- read_csv(paste0(path, "/analogMatch.csv"))%>%
    rename("feature_number" = '#Scan#',
           analog_superclass = superclass, 
           analog_class = class, 
           analog_subclass = subclass)%>%
    select(feature_number, analog_superclass, analog_class, analog_subclass)
  
  csiFingerClassy <- read_csv(paste0(path, '/csiFinger_classyfire.csv'))%>%
    rename(smiles = SMILES)
  
  CSIFingerID <- read_tsv(paste0(path, "/summary_csi_fingerid.tsv"))%>%
    left_join(csiFingerClassy, by = 'smiles')%>%
    rename(feature_number = experimentName,
           csiFinger_superclass = superclass, 
           csiFinger_class = CF_class, 
           csiFinger_subclass = subclass)%>%
    select(feature_number, csiFinger_superclass, csiFinger_class, csiFinger_subclass)%>%
    filter(!is.na(csiFinger_superclass))%>%
    unique()
  
  # metfragClassy <- read_csv(paste0(path, 'MetFragSMILES.csv'))%>%
  #   rename(MetFragSMILES = SMILES,
  #          metfrag_superclass = superclass,
  #          metfrag_class = CF_class,
  #          metfrag_subclass = subclass)%>%
  #   select(MetFragSMILES, metfrag_superclass, metfrag_class, metfrag_subclass)
  # 
  # napClassy <- read_csv(paste0(path, 'NAPSMILES.csv'))%>%
  #   rename(ConsensusSMILES = SMILES,
  #          NAP_superclass = superclass,
  #          NAP_class = CF_class,
  #          NAP_subclass = subclass)%>%
  #   select(ConsensusSMILES, NAP_superclass, NAP_class, NAP_subclass)%>%
  #   unique()
  # 
  # napDf <- read_tsv(paste0(path, "moorea2017_NAP.tsv"))%>%
  #   rename("feature_number" = "cluster.index")%>%
  #   select(feature_number, MetFragSMILES, ConsensusSMILES)%>%
  #   left_join(metfragClassy, by = 'MetFragSMILES')%>%
  #   left_join(napClassy, by = 'ConsensusSMILES')%>%
  #   select(-c(MetFragSMILES, ConsensusSMILES))
  # unique()
  
  canopus <- read_csv(paste0(path, '/canopus_summary.csv'))%>%
    rename(feature_number = scan,
           canopus_superclass = superclass, 
           canopus_class = class, 
           canopus_subclass = subclass)%>%
    select(feature_number, canopus_superclass, canopus_class, canopus_subclass)%>%
    unique()
  
  molnetClassy <- read_csv(paste0(path, "/molNetEnhancer.csv"))%>%
    select(`cluster index`, componentindex, CF_superclass, CF_class, CF_subclass)%>%
    rename(feature_number = "cluster index",
           MolNet_superclass = CF_superclass,
           MolNet_class = CF_class,
           MolNet_subclass = CF_subclass)%>%
    unique()
  
  ecoNet <- read_csv(paste0(path, '/ecoNetConsensus.csv'))%>%
    select(-c(1))%>%
    rename(feature_number = scan)%>%
    filter(!is.na(ecoNetConsensus))%>%
    unique()
  
  combined <- network%>%
    left_join(libraryMatches, by = 'feature_number')%>%
    left_join(analogMatches, by = 'feature_number')%>%
    left_join(CSIFingerID, by = 'feature_number')%>%
    # left_join(napDf, by = 'feature_number')%>%
    left_join(canopus, by = 'feature_number')%>%
    left_join(molnetClassy, by = 'feature_number')%>%
    left_join(ecoNet, by = c('network', 'feature_number'))%>%
    mutate(experiment = name)%>%
    select(experiment, everything())
  
  write_csv(combined, paste0('~/Documents/GitHub/ecoNet/verification/analysis/combined_', name,'.csv'))
}

setwd('~/Documents/GitHub/ecoNet/verification/analysis/')

combined_csv <- dir(path = "~/Documents/GitHub/ecoNet/verification/analysis/", pattern = "*.csv")%>%
  map(read_csv)%>%
  reduce(bind_rows)
  
combined_csv[combined_csv == 'N/A'] <- NA_real_
combined_csv[combined_csv == 'null'] <- NA_real_
combined_csv[combined_csv == 'no matches'] <- NA_real_
combined_csv[combined_csv == 'nan'] <- NA_real_

# VIZUALIZATIONS -- Comparing percent annotation --------------------------
order <- c('Library Matches', 'Analog Matches', 'CSI Finger ID', 'canopus', 'Molnet superclass', 'Molnet class', 'Molnet subclass', 'ecoNetConsensus')
sources <- c('library_superclass', 'analog_superclass', 'csiFinger_superclass', 'canopus_superclass', 'MolNet_superclass', 'MolNet_class', 'MolNet_subclass', 'ecoNetConsensus')

totals <- combined_csv%>%
  select(experiment, network)%>%
  unique()%>%
  group_by(experiment)%>%
  mutate(totalFeatures = 1)%>%
  select(-network)%>%
  summarize_if(is.numeric, sum)


sums <- combined_csv%>%
  select(experiment, network, all_of(sources))%>%
  rename('Library Matches' = 'library_superclass',
         'Analog Matches' = 'analog_superclass',
         'CSI Finger ID' = 'csiFinger_superclass',
         'canopus' = 'canopus_superclass',
         'Molnet superclass' = 'MolNet_superclass',
         'Molnet class' = 'MolNet_class',
         'Molnet subclass' = 'MolNet_subclass')%>%
  gather(annotationSource, annotation, 3:ncol(.))%>%
  mutate(annotationSource = factor(annotationSource),
         annotationSource = fct_relevel(annotationSource, order),
         annotationSource = fct_rev(annotationSource))%>%
  group_by(experiment, network,  annotationSource)%>%
  mutate(annotation = case_when(sum(!is.na(annotation)) > 0 ~ 1,
                                TRUE ~ 0))%>%
  unique()%>%
  ungroup()%>%
  group_by(experiment, annotationSource)%>%
  summarize_if(is.numeric, sum)%>%
  left_join(totals, by = 'experiment')%>%
  mutate(percent = annotation/totalFeatures)
  
sums%>%
  filter(!experiment %like% '%SmallNets')%>%
  ggplot(aes(annotationSource, percent)) +
  geom_bar(stat = 'identity') +
  coord_flip() +
  facet_wrap(~experiment) + 
  labs(x = 'Annotation Source', y = 'Percent of networks annotated') +
  theme(legend.position = 'none',
        plot.margin = unit(c(1,1,1.5,1.2), 'cm'),
        axis.title = element_text(size = 20),
        axis.text.x = element_text(angle = 60, hjust = 1, size = 15),
        axis.text.y = element_text(size = 20),
        plot.title = element_text(size = 15, face = "bold"),
        panel.background = element_rect(fill = "transparent"), # bg of the panel
        plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
        panel.grid.major.y = element_line(size = 0.2, linetype = 'solid',colour = "gray"), # get rid of major grid
        panel.grid.major.x = element_line(size = 0.2, linetype = 'solid',colour = "gray"))






