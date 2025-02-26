library(nflfastR)
library(dplyr)
library(tidyverse)
library(ggrepel)
library(nflreadr)
library(writexl)
library(xlsx)

pbp <- load_pbp(2024) 


## load in player data for 2024 season
players = load_player_stats(seasons=2024)

#rename player items
names(players)[7]="NFL_Team"

#rename passer data
names(players)[12]="Passes Caught"
names(players)[13]="Pass Attempts"
names(players)[14]="Passing Yards"
names(players)[15]="TD Pass"
names(players)[16]="Interceptions Thrown"
names(players)[19]="Passer Fumble"
names(players)[25]="2pt Passing Conversion"

#rename rushing data
names(players)[28]="Rushing Attempts"
names(players)[29]="Rushing Yards"
names(players)[30]="TD Rush"
names(players)[31]="Rushing Fumble"
names(players)[35]="2pt Rushing Conversion"

#rename receiving data
names(players)[36]="Each Reception"
names(players)[37]="Receiving Targets"
names(players)[38]="Receiving Yards"
names(players)[39]="TD Reception"
names(players)[40]="Receiving Fumble"
names(players)[46]="2pt Receiving Conversion"

players <- select(players,c('player_display_name'
                            ,"week"
                            ,'position_group'
                            ,'NFL_Team'
                            ,'headshot_url'
                            ,'Passes Caught'
                            ,"Pass Attempts"
                            ,"Passing Yards"
                            ,"TD Pass"
                            ,"Interceptions Thrown"
                            ,"Passer Fumble"
                            ,"2pt Passing Conversion"
                            , "Rushing Attempts"
                            ,"Rushing Yards"
                            ,"TD Rush"
                            ,"Rushing Fumble"
                            ,"2pt Rushing Conversion"
                            ,"Each Reception"
                            ,"Receiving Targets"
                            ,"Receiving Yards"
                            ,"TD Reception"
                            ,"Receiving Fumble"
                            ,"2pt Receiving Conversion"
                            ))

kickers <- load_player_stats(seasons=2024,stat_type="kicking")
kickers$fg_made_0_39 <- kickers$fg_made_0_19+kickers$fg_made_20_29+kickers$fg_made_30_39
kickers <- kickers %>%
              rename("Each PAT Made"="pat_made",
                     "PAT Attempt"="pat_att",
                     "FG Made (0-39 yards)"="fg_made_0_39",
                     "FG Made (40-49 yards)"="fg_made_40_49",
                     "FG Made (50-59 yards)"="fg_made_50_59",
                     "FG Made (60+ yards)"="fg_made_60_",
                     "Field Goal Attempted"="fg_att",
                     "position_group2"="position_group",
                     "position_group"="position",
                     'NFL_Team'='team'
                     )

kickers <- select(kickers,c('player_display_name'
                            ,'NFL_Team'
                            ,'position_group'
                            ,"week"
                            ,'headshot_url'
                            ,"Each PAT Made"
                            ,"PAT Attempt"
                            ,"FG Made (0-39 yards)"
                            ,"FG Made (40-49 yards)"
                            ,"FG Made (50-59 yards)"
                            ,"FG Made (60+ yards)"
                            ,"Field Goal Attempted"

                            
))

unioned <- bind_rows(kickers,players)              

# nfl_teams <- teams_colors_logos
# write_xlsx(nfl_teams, "nfl.xlsx")

# defense <- load_player_stats(stat_type = "defense")

unique_players = unique(unioned[c("player_display_name","NFL_Team","position_group","headshot_url")])

player2 = c()
nfl_team2 = c()
position2 = c()
week2 = c()
players_all_weeks = data.frame()

for (i in 1:nrow(unique_players)){
  for (j in 1:18){
    player <- unique_players[i,"player_display_name"]
    nfl_team <- unique_players[i,"NFL_Team"]
    position <- unique_players[i,"position_group"]
    headshot <- unique_players[i,"headshot_url"]
    week <- j
    # print(player)
    #rbind(unioned2,list(player))
    #player2 <- append(player2,unique_players[i,"player_display_name"])
    #nfl_team2 <- c(nfl_team2,unique_players[i,"NFL_Team"])
    #position2 <- c(position2,unique_players[i,"position_group"])
    #week2 <- c(week2,j)
    temp = data.frame(a=player,b=nfl_team,c=position,d=headshot,week=week)
    players_all_weeks <- rbind(players_all_weeks,temp)
  }
}
# players_all_weeks = data.frame(player2)
# players_and_weeks <- data.frame(a=c('a'),b=player,c=player2)
# write.xlsx(unioned, "C:/Users/allan/Documents/DS_Projects/Fantasy Football 24/playerstats.xlsx")
# write.xlsx(unique_players, "C:/Users/allan/Documents/DS_Projects/Fantasy Football 24/uniqueplayers.xlsx")
