# Verification of Eco Net consesnsus scores
# Load Libraries
library(tidyverse)
library(DescTools)
library(wesanderson)
library(grDevices)

select <- dplyr::select

gen_theme <-  function(x){
  theme(plot.margin = unit(c(1,1,1.5,1.2), 'cm'),
        axis.title = element_text(size = 25),
        axis.text.x = element_text(angle = 60, hjust = 1, size = 25),
        axis.text.y = element_text(size = 25),
        plot.title = element_text(size = 25, face = "bold"),
        legend.text = element_text(size = 25),
        legend.title = element_text(size = 25),
        panel.background = element_rect(fill = "transparent"), # bg of the panel
        plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
        panel.grid.major.y = element_line(size = 0.2, linetype = 'solid',colour = "gray"), # get rid of major grid
        panel.grid.major.x = element_line(size = 0.2, linetype = 'solid',colour = "gray"))
  }



# Reading in all data which could be gathered from respecrtive dat --------
# set all locations:
path1 <- 'dataset1_unmodified'
path2 <- 'dataset1_NAP'
path3 <- 'dataset1_SmallNets'
path4 <- 'dataset2_unmodified'
path5 <- 'dataset1_FalsePositives'
path6 <- 'dataset2_FalsePositives'
path7 <- 'dataset1_smallNetsFP'
paths <- c(path1, path2, path3, path4, path5, path6, path7)

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
  
  # csiFingerClassy <- read_csv(paste0(path, '/csiFinger_classyfire.csv'))%>%
  #   rename(smiles = SMILES)
  # 
  # CSIFingerID <- read_tsv(paste0(path, "/summary_csi_fingerid.tsv"))%>%
  #   left_join(csiFingerClassy, by = 'smiles')%>%
  #   rename(feature_number = experimentName,
  #          csiFinger_superclass = superclass, 
  #          csiFinger_class = CF_class, 
  #          csiFinger_subclass = subclass)%>%
  #   select(feature_number, csiFinger_superclass, csiFinger_class, csiFinger_subclass)%>%
  #   filter(!is.na(csiFinger_superclass))%>%
  #   unique()
  # 
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
    # left_join(CSIFingerID, by = 'feature_number')%>%
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

baseDf <- combined_csv%>%
  separate(experiment, c('experiment', 'version'), sep = '_')

# VIZUALIZATIONS -- False Positives ---------------------------------------
falsePositive <- baseDf%>%
  select(experiment, version, network, library_superclass, library_class, library_subclass, MolNet_superclass, MolNet_class, MolNet_subclass, ecoNetConsensus)%>%
  gather(annotationSource, annotation, MolNet_superclass:ecoNetConsensus)%>%
  group_by(experiment, version, annotationSource)%>%
  nest()%>%
  mutate(data = map(data, ~ filter(.x, !is.na(library_superclass),
                                   !is.na(annotation))%>%
                      unite(libraryAnnotation, c('library_superclass', 'library_class', 'library_subclass'), sep = ";")%>%
                      rowwise()%>%
                      mutate(congruent = case_when(libraryAnnotation %like% paste0('%', annotation, '%') ~ 1,
                                                   TRUE ~ 0))%>%
                      ungroup()%>%
                      mutate(total = 1,
                             truePositiveRate = sum(congruent)/sum(total))%>%
                      select(truePositiveRate)%>%
                      unique()))%>%
  unnest(data)%>%
  rowwise()%>%
  mutate(annotationSource = case_when(annotationSource %like% 'MolNet%' ~ paste('Molnet', str_split(annotationSource, '_')[[1]][2]),
                                      TRUE ~ annotationSource))

# VIZUALIZATIONS -- Comparing percent annotation --------------------------
order <- c('Library Matches', 'Analog Matches', 'canopus', 'Molnet superclass', 'Molnet class', 'Molnet subclass', 'ecoNetConsensus')
sources <- c('library_superclass', 'analog_superclass', 'canopus_superclass', 'MolNet_superclass', 'MolNet_class', 'MolNet_subclass', 'ecoNetConsensus')

totals <- combined_csv%>%
  select(experiment, network)%>%
  unique()%>%
  group_by(experiment)%>%
  mutate(totalFeatures = 1)%>%
  select(-network)%>%
  summarize_if(is.numeric, sum)%>%
  separate(experiment, c('experiment', 'version'), sep = '_')

sums <- baseDf%>%
  select(experiment, version, network, all_of(sources))%>%
  rename('Library Matches' = 'library_superclass',
         'Analog Matches' = 'analog_superclass',
         # 'CSI Finger ID' = 'csiFinger_superclass',
         'canopus' = 'canopus_superclass',
         'Molnet superclass' = 'MolNet_superclass',
         'Molnet class' = 'MolNet_class',
         'Molnet subclass' = 'MolNet_subclass')%>%
  gather(annotationSource, annotation, 4:ncol(.))%>%
  group_by(experiment, version, network,  annotationSource)%>%
  mutate(annotation = case_when(sum(!is.na(annotation)) > 0 ~ 1,
                                TRUE ~ 0))%>%
  unique()%>%
  ungroup()%>%
  group_by(experiment, version, annotationSource)%>%
  summarize_if(is.numeric, sum)%>%
  left_join(totals, by = c('experiment', 'version'))%>%
  mutate(percent = annotation/totalFeatures*100)%>%
  left_join(falsePositive, by = c('experiment', 'version', 'annotationSource'))%>%
  mutate(truePositives = percent*truePositiveRate,
         falsePositives = percent*(1-truePositiveRate))

# Plotting annotation rates with true positive rates
pdf('~/Documents/GitHub/ecoNet/verification/plots/percentConsensus.pdf', width = 20, height = 10)  
sums%>%
  ungroup()%>%
  filter(version != 'SmallNets')%>%
  mutate(experiment = case_when(version == 'NAP' ~ paste0(experiment, "_", version),
                                TRUE ~ experiment))%>%
  group_by(experiment, annotationSource)%>%
  mutate(std = sd(percent))%>%
  summarize_if(is.numeric, mean)%>%
  ungroup()%>%
  mutate(annotationSource = factor(annotationSource),
         annotationSource = fct_relevel(annotationSource, order),
         annotationSource = fct_rev(annotationSource))%>%
  ggplot(aes(annotationSource, percent)) +
  geom_bar(stat = 'summary', fun.y = 'mean') +
  geom_bar(aes(annotationSource, truePositives, fill = 'Real'), stat = 'summary', fun.y = 'mean', na.rm = TRUE) +
  geom_errorbar(aes(ymax = percent + std, ymin = percent - std)) +
  geom_text(aes(y = percent + 10, label = paste(round(percent, 2), '%')), size = 6) +
  coord_flip() +
  scale_fill_manual(values = '#006658') +
  facet_wrap(~experiment) + 
  labs(x = 'Annotation Source', y = 'Percent of networks annotated', fill = 'True Positives') +
  gen_theme() +
  theme(legend.position = 'None')
dev.off()

fpRates <- sums%>%
  mutate(fpCompare = case_when(version == 'FalsePositives' & annotationSource == 'ecoNetConsensus' ~ 'ecoNet Insilico Consensus',
                               version == 'unmodified' & annotationSource == 'ecoNetConsensus' ~ 'ecoNet Library Consensus',
                               version == 'NAP' ~ paste(annotationSource, 'NAP'),
                               TRUE ~ version))
pdf('~/Documents/GitHub/ecoNet/verification/plots/TruePositives.pdf', width = 20, height = 10)  
fpRates%>%
  filter(version %in% c('unmodified', 'FalsePositives', 'NAP'),
         annotationSource %in% c('ecoNetConsensus', 'Molnet superclass', 'Molnet class', 'Molnet subclass'),
         !fpCompare %in% c('ecoNetConsensus NAP', 'FalsePositives', 'unmodified'))%>%
  ggplot(aes(fpCompare, truePositives, fill = experiment)) +
  geom_bar(aes(y = percent, fill = 'Total Annotations'), stat = 'identity', position = position_dodge2()) +
  geom_bar(stat = 'identity', position = position_dodge2()) +
  scale_fill_manual(values = c(wes_palette('Darjeeling1', n = 5, type = 'discrete')[2:3], 'grey')) +
  labs(x = 'Annotation Source', y = bquote(atop('Percent of networks', 'properly annotated')), fill = 'Experiment') +
  gen_theme()
dev.off()

pdf('~/Documents/GitHub/ecoNet/verification/plots/TruePositiveRate.pdf', width = 20, height = 10)  
fpRates%>%
  filter(version %in% c('unmodified', 'FalsePositives', 'NAP'),
         annotationSource %in% c('ecoNetConsensus', 'Molnet superclass', 'Molnet class', 'Molnet subclass'),
         !fpCompare %in% c('ecoNetConsensus NAP', 'FalsePositives', 'unmodified'))%>%
  ggplot(aes(fpCompare, truePositiveRate*100, fill = experiment)) +
  # geom_bar(aes(y = percent, fill = 'Total Annotations'), stat = 'identity', position = position_dodge2()) +
  geom_bar(stat = 'identity', position = position_dodge2()) +
  scale_fill_manual(values = c(wes_palette('Darjeeling1', n = 5, type = 'discrete')[2:3], 'grey')) +
  labs(x = 'Annotation Source', y = 'True Positive Rate', fill = 'Experiment') +
  gen_theme()
dev.off()

# VIZUALIZATIONS -- EcoNet network size -----------------------------------
# compare number of features annotated by # features annotated
totalFeatures <- combined_csv%>%
  select(experiment)%>%
  group_by(experiment)%>%
  mutate(totalFeatures = 1)%>%
  summarize_if(is.numeric, sum)


netSizeCompare <- combined_csv%>%
  filter(experiment %in% c('dorcierr', 'dorcierrSmallNets'))%>%
  select(experiment, ecoNetConsensus)%>%
  group_by(experiment)%>%
  mutate(ecoNetConsensus = sum(!is.na(ecoNetConsensus)))%>%
  unique()%>%
  ungroup()%>%
  left_join(totalFeatures, by = 'experiment')%>%
  mutate(percent = ecoNetConsensus/totalFeatures)

annotationsLost <- 1-netSizeCompare[2,4]/netSizeCompare[1,4]
annotationsLost 


