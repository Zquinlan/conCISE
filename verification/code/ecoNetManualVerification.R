# LOADING -- packages -------------------------------------------------------
#Data mungering
library(tidyverse)
library(data.table)
library(DescTools)
library(readxl)
library(multcomp)
library(CHNOSZ)
library(ggpubr)
library(rsq)
library(pscl)
library(lme4)

#PCoA, PERMANOVA
library(vegan)
library(ape)

#Visualizations
library(wesanderson)
library(RColorBrewer)
library(ggnewscale)

#Defining functions and removing issues with overlapping function calls
map <- purrr::map
select <- dplyr::select
tidy <- broom::tidy
rename <- dplyr::rename
mutate <- dplyr::mutate

zscore <- function(x) {
  (x-mean(x, na.rm = TRUE))/sd(x, na.rm = TRUE)
}

angular_transform <- function(x) {
  asin(sqrt(x))
}


genTheme <- function(x) {
  theme(
    legend.position = "top",
    legend.text = element_text(size = 20),
    legend.title = element_text(size = 25),
    legend.key = element_rect(fill = "transparent"),
    legend.key.size = unit(3, 'line'),
    legend.box= "vertical",
    plot.margin = unit(c(1,1,1.5,1.2), 'cm'),
    # plot.margin = margin(2,.8,2,.8, "cm"),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30),
    axis.title = element_text(size = 30),
    panel.background = element_rect(fill = "transparent"), # bg of the panel
    plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
    panel.grid.major = element_blank(), # get rid of major grid
    panel.grid.minor = element_blank()) # get rid of minor grid
}


# Loading -- raw manual verification ---------------------------------------
rawEcoNet <- read_csv('conCISEVerification.csv')%>%
  rename(checkCanopus = `manual check - CANOPUS`,
         checkLibrary = `manual check - Library`)%>%
  mutate(checkLibrary = case_when(checkLibrary == 'correct - sesquiterpene' ~ 'correct',
                                  checkLibrary == 'correct?' ~ 'correct',
                                  checkLibrary == 'not correct?' ~ 'incorrect',
                                  checkLibrary == 'Not correct?' ~ 'incorrect',
                                  checkLibrary == 'incorrect?' ~ 'incorrect',
                                  checkLibrary == 'incorrect? - saturated' ~ 'incorrect',
                                  checkLibrary == '?' ~ 'incorrect',
                                  checkLibrary == 'correct (norterpenoid)' ~ 'correct',
                                  TRUE ~ checkLibrary),
         checkCanopus = case_when(checkCanopus == 'correct - sesquiterpene' ~ 'correct',
                                  checkCanopus == 'correct?' ~ 'correct',
                                  checkCanopus == 'not correct?' ~ 'incorrect',
                                  checkCanopus == 'Not correct?' ~ 'incorrect',
                                  checkCanopus == 'incorrect?' ~ 'incorrect',
                                  checkLibrary == 'incorrect? - saturated' ~ 'incorrect',
                                  checkCanopus == '?' ~ 'incorrect',
                                  TRUE ~ checkCanopus))


# Vizualizing -------------------------------------------------------------
libraryCount <- rawEcoNet%>%
  filter(!is.na(checkCanopus), 
         !is.na(checkLibrary),
         !is.na(ecoNetConsensusLevelLibrary))%>%
  # filter(ecoNetConsensusScoreCanopus >= 0.7)%>%
  select(experiment, checkLibrary, ecoNetConsensusLevelLibrary)%>%
  group_by(experiment, checkLibrary, ecoNetConsensusLevelLibrary)%>%
  mutate(count = 1)%>%
  summarize_if(is.numeric, sum)%>%
  ungroup()%>%
  group_by(experiment, ecoNetConsensusLevelLibrary)%>%
  mutate(percent = count/sum(count)*100)%>%
  group_by(checkLibrary, ecoNetConsensusLevelLibrary)%>%
  mutate(std = sd(percent))%>%
  summarize_if(is.numeric, mean, na.rm = TRUE)%>%
  ungroup()%>%
  rename(ecoNetConsensusLevel = ecoNetConsensusLevelLibrary,
         check = checkLibrary)%>%
  mutate(source = 'Spectral library match')

canopusCount <- rawEcoNet%>%
  filter(!is.na(checkCanopus), 
         !is.na(checkLibrary),
         !is.na(ecoNetConsensusLevelCanopus))%>%
  # filter(ecoNetConsensusScoreCanopus >= 0.7)%>%
  select(experiment, checkCanopus, ecoNetConsensusLevelCanopus)%>%
  group_by(experiment, checkCanopus, ecoNetConsensusLevelCanopus)%>%
  mutate(count = 1)%>%
  summarize_if(is.numeric, sum)%>%
  ungroup()%>%
  group_by(experiment, ecoNetConsensusLevelCanopus)%>%
  mutate(percent = count/sum(count)*100)%>%
  group_by(checkCanopus, ecoNetConsensusLevelCanopus)%>%
  mutate(std = sd(percent))%>%
  summarize_if(is.numeric, mean, na.rm = TRUE)%>%
  ungroup()%>%
  rename(ecoNetConsensusLevel = ecoNetConsensusLevelCanopus,
         check = checkCanopus)%>%
  mutate(source = 'CANOPUS')

countEverything <- libraryCount%>%
  bind_rows(canopusCount)%>%
  mutate(vjust = case_when(ecoNetConsensusLevel == 'superclass' & source == 'Spectral library match' ~ -2.4,
                           TRUE ~ -2.2),
         hjust = case_when(ecoNetConsensusLevel == 'class' ~ 0.6,
                           ecoNetConsensusLevel == 'subclass' ~ 0.7,
                             TRUE ~ 0.5))

countEverything%>% 
  filter(check == 'correct')%>%
  group_by(source)
  

pdf('~/Documents/GitHub/ecoNet/verification/plots/ConCISECanopusVerification.pdf', width = 10, height = 10)
countEverything%>%
  mutate(ecoNetConsensusLevel = as.factor(ecoNetConsensusLevel),
         ecoNetConsensusLevel = fct_relevel(ecoNetConsensusLevel, 'superclass'),
         source = as.factor(source),
         source = fct_relevel(source, 'Spectral library match'))%>%
  filter(check == 'correct')%>%
  ggplot(aes(source, percent, fill = ecoNetConsensusLevel)) +
  geom_errorbar(aes(ymax = percent + std, ymin = percent - std), position = 'dodge') +
  geom_bar(stat = 'identity', position = 'dodge') +
  geom_text(aes(label = paste(round(percent, 2), '%'), vjust = vjust, hjust = hjust), position = position_dodge2(width = 1), size = 6) +
  genTheme() +
  scale_fill_manual(values = c('#332288', '#88CCEE', '#CC6677')) +
  labs(y = 'True positive rate', x = 'ConCISE annotation source', fill = 'ConCISE consensus level') +
  scale_y_continuous(limits = c(0,110), breaks = c(0,25,50,75,100))
dev.off()


