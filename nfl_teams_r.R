library(nflfastR)
library(dplyr)
library(tidyverse)
library(ggrepel)
library(nflreadr)
library(writexl)
library(xlsx)

pbp <- load_pbp(2024) 

nfl_teams <- teams_colors_logos
write.xlsx(nfl_teams, "C:/Users/allan/Documents/DS_Projects/Fantasy Football 24/nflTeams.xlsx")
