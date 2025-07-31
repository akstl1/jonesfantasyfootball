from espn_api.football import League
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()


###############################
###############################
### Load in League Settings ###
###############################
###############################

league = League(league_id=os.getenv("LEAGUE_ID"), year=int(os.getenv("YEAR")), espn_s2=os.getenv("S2"),swid=os.getenv("SWID"))

def curr_week():
    curr_week=league.current_week
    return curr_week

def fantasy_teams():
    teams = league.teams
    fantasyTeams_df = pd.DataFrame({
        'Manager Name':[],
        'Fantasy Name':[],
        'Acronym':[],
        'Division':[],
        'Image':[]
    })
    for team in teams:
        manager = team.owners[0]['firstName'][0]+team.owners[0]['lastName'][0]
        fantasy = team.team_name
        acronym = team.team_abbrev
        division = team.division_name
        image = team.logo_url
        new_row = pd.DataFrame({
        'Manager Name':[manager],
        'Fantasy Name':[fantasy],
        'Acronym':[acronym],
        'Division':[division],
        'Image':[image]
        })
        fantasyTeams_df = pd.concat([fantasyTeams_df,new_row],ignore_index=True)
    fantasyTeams_df.to_excel('fantasyTeams_df.xlsx', sheet_name='Sheet1', index=False)

###############################
###############################
###### Helper Functions #######
###############################
###############################


def hundredyardgame(value):
    if value<100 or value>199:
        return 0
    else:
        return 1
def threehundredyardpassinggame(value):
    if value<300 or value>399:
        return 0
    else:
        return 1
    

###############################
###############################
### Run after draft is over ###
###############################
###############################

##### draft data


def draft(players=12,rounds=17):
    draft_df = pd.DataFrame({'Team':[],'Player':[],'Round':[],'Pick':[]})

    for i in range(players*rounds):
        new_row = pd.DataFrame({'Team':[league.draft[i].team.team_name],'Player':[league.draft[i].playerName],'Round':[league.draft[i].round_num],'Pick':[league.draft[i].round_pick]})
        draft_df = pd.concat([draft_df,new_row],ignore_index=True)
    draft_df.to_excel('draft.xlsx', sheet_name='Sheet1', index=False)


###############################
###############################
### Individual Week Queries ###
###############################
###############################

##### power rankings data

def powerRankingsSingleWeek(current_wk=curr_week,players=12):
    power_ranking_df = pd.DataFrame({'Team':[],'Week':[],'Rank':[]})
    rankings = league.power_rankings(week=current_wk)
    for rank in range(players):
        team = rankings[rank][1].team_name
        ranking = rank+1
        new_row = pd.DataFrame({'Team':[team],'Week':[current_wk],'Rank':[ranking]})
        power_ranking_df = pd.concat([power_ranking_df,new_row],ignore_index=True)
    # print(power_ranking_df)
    power_ranking_df.to_excel('power_rankingWk'+str(current_wk)+'.xlsx', sheet_name='Sheet1', index=False)

##### standings data

def standingsSingleWeek(current_wk=curr_week, players=12):
    standings_df = pd.DataFrame({'Team':[],'Week':[],'League_Rank':[],'Division_Rank':[]})
    standings = league.standings_weekly(current_wk)
    travis = 1
    taylor = 1
    for rank in range(players):
        team = standings[rank].team_name
        league_ranking = rank+1
        if standings[rank].division_name=="Team Travis":
            div_standing = travis
            travis+=1
        else:
            div_standing = taylor
            taylor+=1
        new_row = pd.DataFrame({'Team':[team],'Week':[current_wk],'League_Rank':[league_ranking],'Division_Rank':[div_standing]})
        standings_df = pd.concat([standings_df,new_row],ignore_index=True)

    # print(standings_df)
    standings_df.to_excel('standingsWk'+str(current_wk)+'.xlsx', sheet_name='Sheet1', index=False)

##### matchup data

def matchupsSingleWeek(current_wk=curr_week,players=12):
    matchups_df = pd.DataFrame({'Team':[],
                            'Opponent':[],
                            'Week':[],
                            'Home_Or_Away':[],
                            'Projected Points':[],
                            'Actual Points':[],
                            'matchup_type':[],
                            'projected_variance':[],
                            'actual_variance':[],
                            'Matchup Header':[],
                            'Result':[],
                            'Number':[],
                            'MatchupKey':[],
                            'WeeklyMatchupID':[],
                            'ID':[]
                            })
    box_score = league.box_scores(current_wk)
    bye_counter=1
    if current_wk==15:
        matchups = 7
    else:
        matchups = 6
    for matchup in range(matchups):
        home_team = box_score[matchup].home_team
        home_projected = box_score[matchup].home_projected
        home_actual = box_score[matchup].home_score

        away_team = box_score[matchup].away_team
        
        if away_team==0:
            away_tm = 'Bye'
            matchupkeyaway = str(current_wk)+away_tm+str(bye_counter)
            bye_counter+=1
            
        else:
            away_tm = away_team.team_name
            matchupkeyaway = str(current_wk)+away_tm
        away_projected = box_score[matchup].away_projected
        away_actual = box_score[matchup].away_score  
        header = home_team.team_name + " vs. " + away_tm
        matchup_type = box_score[matchup].matchup_type

        if home_actual - away_actual>0:
            result_home, result_away='Win','Loss'
        elif  home_actual - away_actual <0:
            result_home, result_away='Loss','Win'
        else:
            result_home, result_away = 'Tie', 'Tie'
        new_row_home = pd.DataFrame({
                            'Team':[home_team.team_name],
                            'Opponent':[away_tm],
                            'Week':[current_wk],
                            'Home_Or_Away':['Home'],
                            'Projected Points':[home_projected],
                            'Actual Points':[home_actual],
                            'matchup_type':[matchup_type],
                            'projected_variance':[home_projected-away_projected],
                            'actual_variance':[home_actual-away_actual],
                            'Matchup Header':[header],
                            'Result':[result_home],
                            'Number':2,
                            'MatchupKey':str(current_wk)+home_team.team_name,
                            'ID':matchup+7,
                            'WeeklyMatchupID':matchup+1
                            })
        
        new_row_away = pd.DataFrame({
                            'Team':[away_tm],
                            'Opponent':[home_team.team_name],
                            'Week':[current_wk],
                            'Home_Or_Away':['Away'],
                            'Projected Points':[away_projected],
                            'Actual Points':[away_actual],
                            'matchup_type':[matchup_type],
                            'projected_variance':[away_projected-home_projected],
                            'actual_variance':[away_actual-home_actual],
                            'Matchup Header':[header],
                            'Result':[result_away],
                            'Number':1,
                            'MatchupKey':matchupkeyaway,
                            'ID':matchup+1,
                            'WeeklyMatchupID':matchup+1
                            })
        new_row_home['projected_variance'] = new_row_home['projected_variance'].round(2)
        new_row_home['actual_variance'] = new_row_home['actual_variance'].round(2)

        new_row_away['projected_variance'] = new_row_away['projected_variance'].round(2)
        new_row_away['actual_variance'] = new_row_away['actual_variance'].round(2)

        matchups_df = pd.concat([matchups_df,new_row_home],ignore_index=True)
        matchups_df = pd.concat([matchups_df,new_row_away],ignore_index=True)

        matchups_df.to_excel('matchupsWk'+str(current_wk)+'.xlsx', sheet_name='Sheet1', index=False)

        # print(matchups_df)


def playerStatsSingleWeek(current_wk=curr_week,players=12):
    player_df = pd.DataFrame({  
                            'Week':[],
                            'FantasyTeam':[],
                            'Player Name':[],
                            'PlayerID':[],
                            'Headshot_url':[],
                            'Status':[],
                            'NFL_Team':[],
                            'Opponent':[],
                            'Position':[],
                            'PositionRank':[],
                            'Lineup Slot':[],
                            'PlayerKey':[],
                            'Bye':[],
                            'Home':[],
                            'Projected':[],
                            'Each PAT Made':[],
                            'PAT Attempt':[],
                            'FG Made (0-39 yards)':[],
                            'FG Made (40-49 yards)':[],
                            'FG Made (50-50 yards)':[],
                            'FG Made (60+ yards)':[],
                            'Field Goal Attempted':[],
                            'Passes Caught':[],
                            'Pass Attempts':[],
                            'Passing Yards':[],
                            'TD Pass':[],
                            'Interceptions Thrown':[],
                            'Passer Fumble':[],
                            '2pt Passing Conversion':[],
                            'Rushing Attempts':[],
                            'Rushing Yards':[],
                            'TD Rush':[],
                            'Rushing Fumble':[],
                            '2pt Rushing Conversion':[],
                            'Each Reception':[],
                            'Receiving Targets':[],
                            'Receiving Yards':[],
                            'TD Reception':[],
                            'Receiving Fumble':[],
                            '2pt Receiving Conversion':[],
                            'Each Sack':[],
                            'Interception Return TD':[],
                            'Fumble Return TD':[],
                            'Kickoff Return TD':[],
                            'Punt Return TD':[],
                            'Blocked Punt or FG return for TD':[],
                            'Blocked Punt, PAT or FG':[],
                            'Each Interception':[],
                            'Each Fumble Recovered':[],
                            'Each Safety':[],
                            '0 points allowed':[],
                            '1-6 points allowed':[],
                            '7-13 points allowed':[],
                            '14-17 points allowed':[],
                            '28-34 points allowed':[],
                            '35-45 points allowed':[],
                            '46+ points allowed':[],
                            'Less than 100 total yards allowed':[],
                            '100-199 total yards allowed':[],
                            '200-299 yards allowed':[],
                            '350-399 yards allowed':[],
                            '400-449 yards allowed':[],
                            '450-499 yards allowed':[],
                            '500-549 yards allowed':[],
                            '550+ yards allowed':[],
                            '2pt Return':[],
                            '1pt Safety':[],
                            'Defense Fumbles Lost':[],
                            'Actual':[],
                            'Fumble Recovered for TD':[]
                            })
    box_score = league.box_scores(current_wk)
    player_wk=current_wk
    print(current_wk)
    if current_wk==15:
        matchups = 7
    else:
        matchups = 6
    for matchup in range(matchups):
        for i in ['home','away']:
            wrNum = 1
            rbNum = 1
            beNum = 1
            for player in range(17):
                if box_score[matchup].away_team==0:
                    pass
                else:
                    empty=0
                    if i =='home':
                        try:
                            player_name_home = box_score[matchup].home_lineup[player].name
                            # print(player_name_home, player_wk)
                            player_id = box_score[matchup].home_lineup[player].playerId
                            plyr = box_score[matchup].home_lineup[player]
                            team = box_score[matchup].home_team.team_name
                            bye = box_score[matchup].home_lineup[player].on_bye_week
                            status = box_score[matchup].home_lineup[player].active_status
                            pos = plyr.position
                            player_key = str(player_wk)+player_name_home
                            home='1'
                            slotTemp = box_score[matchup].home_lineup[player].lineupSlot
                            if slotTemp == 'RB/WR/TE':
                                slot = 'Flex'
                            elif slotTemp == 'RB':
                                slot = slotTemp+str(rbNum)
                                rbNum+=1
                            elif slotTemp == 'WR':
                                slot = slotTemp+str(wrNum)
                                wrNum+=1
                            elif slotTemp == 'BE':
                                slot = slotTemp+str(beNum)
                                beNum+=1
                            else:
                                slot = slotTemp
                            if pos != 'D/ST':
                                headshot = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/"+str(player_id)+".png&w=96&h=70&cb=1"
                            else:
                                headshot = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/"+plyr.proTeam.lower()+".png&h=50&w=50"
                        except IndexError:
                            empty=1
                    else:
                        try:
                            player_name_home = box_score[matchup].away_lineup[player].name
                            # print(player_name_home, player_wk)
                            player_id = box_score[matchup].away_lineup[player].playerId
                            plyr = box_score[matchup].away_lineup[player]
                            team = box_score[matchup].away_team.team_name
                            bye = box_score[matchup].away_lineup[player].on_bye_week
                            status = box_score[matchup].away_lineup[player].active_status
                            pos = plyr.position
                            player_key = str(player_wk)+player_name_home
                            home='0'
                            slotTemp = box_score[matchup].away_lineup[player].lineupSlot
                            if slotTemp == 'RB/WR/TE':
                                slot = 'Flex'
                            elif slotTemp == 'RB':
                                slot = slotTemp+str(rbNum)
                                rbNum+=1
                            elif slotTemp == 'WR':
                                slot = slotTemp+str(wrNum)
                                wrNum+=1
                            elif slotTemp == 'BE':
                                slot = slotTemp+str(beNum)
                                beNum+=1
                            else:
                                slot = slotTemp
                            if pos != 'D/ST':
                                headshot = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/"+str(player_id)+".png&w=96&h=70&cb=1"
                            else:
                                headshot = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/"+plyr.proTeam.lower()+".png&h=50&w=50"
                        except IndexError:
                            empty=1
                    qb,rb,other = '','',''
                    if pos=='QB':
                        qb,rb,other='lostFumbles','junk','junk'
                    elif pos=='RB':
                        qb,rb,other='junk','lostFumbles','junk'
                    else:
                        qb,rb,other='junk','junk','lostFumbles'
                    temp = []
                    stats = [
                        'madeExtraPoints',
                        'attemptedExtraPoints',
                        'madeFieldGoalsFromUnder40',
                        'madeFieldGoalsFrom40To49',
                        'madeFieldGoalsFrom50Plus',
                        'madeFieldGoalsFrom60Plus',
                        # 'madeFieldGoals',
                        'attemptedFieldGoals',
                        'passingCompletions',
                        'passingAttempts',
                        'passingYards',
                        'passingTouchdowns',
                        'passingInterceptions',
                        qb,
                        'passing2PtConversions',
                        'rushingAttempts',
                        'rushingYards',
                        'rushingTouchdowns',
                        rb,
                        'rushing2PtConversions',
                        'receivingReceptions',
                        'receivingTargets',
                        'receivingYards',
                        'receivingTouchdowns',
                        other,
                        'receiving2PtConversions',
                        'defensiveSacks',
                        'interceptionReturnTouchdowns',
                        'fumbleReturnTouchdowns',
                        'kickoffReturnTouchdowns',
                        'puntReturnTouchdowns',
                        'defensiveBlockedKickForTouchdowns',
                        'defensiveBlockedKicks',
                        'defensiveInterceptions',
                        'defensiveFumbles',
                        'defensiveSafeties',
                        'defensive0PointsAllowed',
                        'defensive1To6PointsAllowed',
                        'defensive7To13PointsAllowed',
                        'defensive14To17PointsAllowed',
                        'defensive28To34PointsAllowed',
                        'defensive35To45PointsAllowed',
                        'defensive45PlusPointsAllowed',
                        'defensiveLessThan100YardsAllowed',
                        'defensive100To199YardsAllowed',
                        'defensive200To299YardsAllowed',
                        # 'defensive300To349YardsAllowed',
                        'defensive350To399YardsAllowed',
                        'defensive400To449YardsAllowed',
                        'defensive450To499YardsAllowed',
                        'defensive500To549YardsAllowed',
                        'defensive550PlusYardsAllowed',
                        # '2pt Return':[],
                        'junk',
                        'junk', #1pt safety
                        'junk' #'defensiveFumbles'/,
                        ,'fumbleRecoveredForTD'
                        ]
                    if (not(bye) and status!='bye' and empty==0): ## or (player_id==8439 and player_wk!=12) or (player_id==3116593 and player_wk!=7) or (player_id==3051392 and player_wk!=7) or (player_id==2980453 and player_wk!=12) or (player_id==3051926 and player_wk!=5)  or (player_id==2577327 and player_wk!=10) or (player_id==11122 and player_wk!=11) or (player_id==4241457 and player_wk!=9)  or (player_id==4360569 and player_wk!=9 and player_wk<=13)  or (player_id==4361579 and player_wk!=14) or (player_id==3912547 and player_wk!=6) or (player_id==2977187 and player_wk!=6) or (player_id==3051876 and player_wk!=12) or (player_id==3126486 and player_wk!=9)
                        for item in stats:
                            try:
                                value=plyr.points_breakdown[item]
                            except KeyError:
                                value=0
                            temp.append(value)
                        player_row_home = pd.DataFrame({
                                'Week':[player_wk],
                                'FantasyTeam':[team],
                                'Player Name':[player_name_home],
                                'PlayerID':[player_id],
                                'Headshot_url':[headshot],
                                'NFL_Team':[plyr.proTeam],
                                'Status':[plyr.active_status],
                                'Opponent':[plyr.pro_opponent],
                                'Position':[plyr.position],
                                'PositionRank':[plyr.posRank],
                                'Lineup Slot': [slot],
                                'PlayerKey':[player_key],
                                'Home':[home],
                                'Bye':[plyr.on_bye_week],
                                'Projected':[plyr.projected_points],
                                'Each PAT Made':temp[0],
                                'PAT Attempt':temp[1],
                                'FG Made (0-39 yards)':temp[2],
                                'FG Made (40-49 yards)':temp[3],
                                'FG Made (50-59 yards)':temp[4] - temp[5],
                                'FG Made (60+ yards)':temp[5],
                                'Field Goal Attempted':temp[6],
                                'Passes Caught':temp[7],
                                'Pass Attempts':temp[8],
                                'Passing Yards':temp[9],
                                'TD Pass':temp[10],
                                'Interceptions Thrown':temp[11],
                                'Passer Fumble':temp[12],
                                '2pt Passing Conversion':temp[13],
                                'Rushing Attempts':temp[14],
                                'Rushing Yards':temp[15],
                                'TD Rush':temp[16],
                                'Rushing Fumble':temp[17],
                                '2pt Rushing Conversion':temp[18],
                                'Each Reception':temp[19],
                                'Receiving Targets':temp[20],
                                'Receiving Yards':temp[21],
                                'TD Reception':temp[22],
                                'Receiving Fumble':temp[23],
                                '2pt Receiving Conversion':temp[24],
                                'Each Sack':temp[25],
                                'Interception Return TD':temp[26],
                                'Fumble Return TD':temp[27],
                                'Kickoff Return TD':temp[28],
                                'Punt Return TD':temp[29],
                                'Blocked Punt or FG return for TD':temp[30],
                                'Blocked Punt, PAT or FG':temp[31],
                                'Each Interception':temp[32],
                                'Each Fumble Recovered':temp[33],
                                'Each Safety':temp[34],
                                '0 points allowed':temp[35],
                                '1-6 points allowed':temp[36],
                                '7-13 points allowed':temp[37],
                                '14-17 points allowed':temp[38],
                                '28-34 points allowed':temp[39],
                                '35-45 points allowed':temp[40],
                                '46+ points allowed':temp[41],
                                'Less than 100 total yards allowed':temp[42],
                                '100-199 total yards allowed':temp[43],
                                '200-299 yards allowed':temp[44],
                                '350-399 yards allowed':temp[45],
                                '400-449 yards allowed':temp[46],
                                '450-499 yards allowed':temp[47],
                                '500-549 yards allowed':temp[48],
                                '550+ yards allowed':temp[49],
                                '2pt Return':0,
                                '1pt Safety':temp[51],
                                'Defense Fumbles Lost':temp[52],
                                'Actual':[plyr.points],
                                'Fumble Recovered for TD':temp[53]
                                })

                        player_df = pd.concat([player_df,player_row_home],ignore_index=True)
                    elif empty==1:
                        pass
                    else:
                        player_row_bye = pd.DataFrame({
                                'Week':[player_wk],
                                'FantasyTeam':[team],
                                'Player Name':[player_name_home],
                                'PlayerID':[player_id],
                                'Headshot_url':[headshot],
                                'NFL_Team':[plyr.proTeam],
                                'Status':[plyr.active_status],
                                'Opponent':[plyr.pro_opponent],
                                'Position':[plyr.position],
                                'PositionRank':[plyr.posRank],
                                'PlayerKey':[player_key],
                                'Lineup Slot': [slot],
                                'Home':'Bye',
                                'Bye':1,
                                'Projected':0,
                                'Each PAT Made':0,
                                'PAT Attempt':0,
                                'FG Made (0-39 yards)':0,
                                'FG Made (40-49 yards)':0,
                                'FG Made (50-50 yards)':0,
                                'FG Made (60+ yards)':0,
                                'Field Goal Attempted':0,
                                'Passes Caught':0,
                                'Pass Attempts':0,
                                'Passing Yards':0,
                                'TD Pass':0,
                                'Interceptions Thrown':0,
                                'Passer Fumble':0,
                                '2pt Passing Conversion':0,
                                'Rushing Attempts':0,
                                'Rushing Yards':0,
                                'TD Rush':0,
                                'Rushing Fumble':0,
                                '2pt Rushing Conversion':0,
                                'Each Reception':0,
                                'Receiving Targets':0,
                                'Receiving Yards':0,
                                'TD Reception':0,
                                'Receiving Fumble':0,
                                '2pt Receiving Conversion':0,
                                'Each Sack':0,
                                'Interception Return TD':0,
                                'Fumble Return TD':0,
                                'Kickoff Return TD':0,
                                'Punt Return TD':0,
                                'Blocked Punt or FG return for TD':0,
                                'Blocked Punt, PAT or FG':0,
                                'Each Interception':0,
                                'Each Fumble Recovered':0,
                                'Each Safety':0,
                                '0 points allowed':0,
                                '1-6 points allowed':0,
                                '7-13 points allowed':0,
                                '14-17 points allowed':0,
                                '28-34 points allowed':0,
                                '35-45 points allowed':0,
                                '46+ points allowed':0,
                                'Less than 100 total yards allowed':0,
                                '100-199 total yards allowed':0,
                                '200-299 yards allowed':0,
                                '350-399 yards allowed':0,
                                '400-449 yards allowed':0,
                                '450-499 yards allowed':0,
                                '500-549 yards allowed':0,
                                '550+ yards allowed':0,
                                '2pt Return':0,
                                '1pt Safety':0,
                                'Defense Fumbles Lost':0,
                                'Actual':0,
                                'Fumble Recovered for TD':0
                                })

                        player_df = pd.concat([player_df,player_row_bye],ignore_index=True)
                    empty=0


    player_df['100-199 yard receiving game'] = player_df['Receiving Yards'].map(hundredyardgame)
    player_df['100-199 yard rushing game'] = player_df['Rushing Yards'].map(hundredyardgame)
    player_df['300-399 yard passing game'] = player_df['Passing Yards'].map(threehundredyardpassinggame)
    player_df_new = pd.melt(player_df,id_vars=['Week','FantasyTeam','Player Name','PlayerID','Headshot_url','Status','NFL_Team','Opponent','Position','PositionRank','PlayerKey','Bye','Projected','Actual', 'Home', 'Lineup Slot'],var_name='Attribute',value_name='Value')
    player_df_final = pd.DataFrame(player_df_new)


    ##### player stats data

    players_table = player_df_final[['Week','FantasyTeam','NFL_Team','Player Name','Status','Home','Lineup Slot','PlayerKey']].copy()

    players_table = players_table.drop_duplicates()

    players_table['MatchupKey'] = players_table.apply(lambda row: str(row['Week'])[0]+row['FantasyTeam'] if row['Week']<10 else str(row['Week'])[:2]+row['FantasyTeam'],axis=1)
    player_df_final.to_excel('playerpointsnewWk'+str(current_wk)+'.xlsx',sheet_name='Sheet1',index=False)
    players_table.to_excel('playerstableWk'+str(current_wk)+'.xlsx',sheet_name='Sheet1',index=False)
    # player_df_final.to_excel('playerpointsnew.xlsx',sheet_name='Sheet1',index=False)



###############################
###############################
#### Season-to-date queries ###
###############################
###############################


##### power rankings data

def powerRankingsMultiWeek(current_wk=curr_week,start_wk=1,players=12):
    for wk in range(start_wk,current_wk+1):
        power_ranking_df = pd.DataFrame({'Team':[],'Week':[],'Rank':[]})
        rankings = league.power_rankings(week=wk)
        for rank in range(players):
            team = rankings[rank][1].team_name
            ranking = rank+1
            new_row = pd.DataFrame({'Team':[team],'Week':[wk],'Rank':[ranking]})
            power_ranking_df = pd.concat([power_ranking_df,new_row],ignore_index=True)
        # print(power_ranking_df)
        power_ranking_df.to_excel('power_rankingWk'+str(wk)+'.xlsx', sheet_name='Sheet1', index=False)


##### standings data

def standingsMultiWeek(start_wk=1,current_wk=curr_week,players=12):
    for wk in range(start_wk,current_wk+1):
        standings_df = pd.DataFrame({'Team':[],'Week':[],'League_Rank':[],'Division_Rank':[]})
        standings = league.standings_weekly(wk)
        travis = 1
        taylor = 1
        for rank in range(players):
            team = standings[rank].team_name
            league_ranking = rank+1
            if standings[rank].division_name=="Team Travis":
                div_standing = travis
                travis+=1
            else:
                div_standing = taylor
                taylor+=1
            new_row = pd.DataFrame({'Team':[team],'Week':[wk],'League_Rank':[league_ranking],'Division_Rank':[div_standing]})
            standings_df = pd.concat([standings_df,new_row],ignore_index=True)

        # print(standings_df)
        standings_df.to_excel('standingsWk'+str(wk)+'.xlsx', sheet_name='Sheet1', index=False)



##### matchup data

def matchupsMultiWeek(start_wk=1,current_wk=curr_week,players=12):
    for wk in range(start_wk,current_wk+1):
        matchups_df = pd.DataFrame({'Team':[],
                            'Opponent':[],
                            'Week':[],
                            'Home_Or_Away':[],
                            'Projected Points':[],
                            'Actual Points':[],
                            'matchup_type':[],
                            'projected_variance':[],
                            'actual_variance':[],
                            'Matchup Header':[],
                            'Result':[],
                            'Number':[],
                            'MatchupKey':[],
                            'WeeklyMatchupID':[],
                            'ID':[]
                            })
        box_score = league.box_scores(wk)
        week=wk
        bye_counter=1
        if wk==15:
            matchups = 7
        else:
            matchups = 6
        for matchup in range(matchups):
            home_team = box_score[matchup].home_team
            home_projected = box_score[matchup].home_projected
            home_actual = box_score[matchup].home_score

            away_team = box_score[matchup].away_team
        
            if away_team==0:
                away_tm = 'Bye'
                matchupkeyaway = str(wk)+away_tm+str(bye_counter)
                bye_counter+=1
            
            else:
                away_tm = away_team.team_name
                matchupkeyaway = str(wk)+away_tm
            away_projected = box_score[matchup].away_projected
            away_actual = box_score[matchup].away_score  
            header = home_team.team_name + " vs. " + away_tm
            matchup_type = box_score[matchup].matchup_type

            if home_actual - away_actual>0:
                result_home, result_away='Win','Loss'
            elif  home_actual - away_actual <0:
                result_home, result_away='Loss','Win'
            else:
                result_home, result_away = 'Tie', 'Tie'
            new_row_home = pd.DataFrame({
                            'Team':[home_team.team_name],
                            'Opponent':[away_tm],
                            'Week':[wk],
                            'Home_Or_Away':['Home'],
                            'Projected Points':[home_projected],
                            'Actual Points':[home_actual],
                            'matchup_type':[matchup_type],
                            'projected_variance':[home_projected-away_projected],
                            'actual_variance':[home_actual-away_actual],
                            'Matchup Header':[header],
                            'Result':[result_home],
                            'Number':2,
                            'MatchupKey':str(week)+home_team.team_name,
                            'ID':matchup+7,
                            'WeeklyMatchupID':matchup+1
                            })
        
            new_row_away = pd.DataFrame({
                            'Team':[away_tm],
                            'Opponent':[home_team.team_name],
                            'Week':[wk],
                            'Home_Or_Away':['Away'],
                            'Projected Points':[away_projected],
                            'Actual Points':[away_actual],
                            'matchup_type':[matchup_type],
                            'projected_variance':[away_projected-home_projected],
                            'actual_variance':[away_actual-home_actual],
                            'Matchup Header':[header],
                            'Result':[result_away],
                            'Number':1,
                            'MatchupKey':matchupkeyaway,
                            'ID':matchup+1,
                            'WeeklyMatchupID':matchup+1
                            })
            new_row_home['projected_variance'] = new_row_home['projected_variance'].round(2)
            new_row_home['actual_variance'] = new_row_home['actual_variance'].round(2)

            new_row_away['projected_variance'] = new_row_away['projected_variance'].round(2)
            new_row_away['actual_variance'] = new_row_away['actual_variance'].round(2)

            matchups_df = pd.concat([matchups_df,new_row_home],ignore_index=True)
            matchups_df = pd.concat([matchups_df,new_row_away],ignore_index=True)

        matchups_df.to_excel('matchupsWk'+str(wk)+'.xlsx', sheet_name='Sheet1', index=False)

            # print(matchups_df)



##### player stats data

def playerStatsMultiWeek(start_wk=1,current_wk=curr_week,players=12):
    for wk in range(start_wk,current_wk+1):
        player_df = pd.DataFrame({  
                            'Week':[],
                            'FantasyTeam':[],
                            'Player Name':[],
                            'PlayerID':[],
                            'Headshot_url':[],
                            'Status':[],
                            'NFL_Team':[],
                            'Opponent':[],
                            'Position':[],
                            'PositionRank':[],
                            'Lineup Slot':[],
                            'PlayerKey':[],
                            'Bye':[],
                            'Home':[],
                            'Projected':[],
                            'Each PAT Made':[],
                            'PAT Attempt':[],
                            'FG Made (0-39 yards)':[],
                            'FG Made (40-49 yards)':[],
                            'FG Made (50-50 yards)':[],
                            'FG Made (60+ yards)':[],
                            'Field Goal Attempted':[],
                            'Passes Caught':[],
                            'Pass Attempts':[],
                            'Passing Yards':[],
                            'TD Pass':[],
                            'Interceptions Thrown':[],
                            'Passer Fumble':[],
                            '2pt Passing Conversion':[],
                            'Rushing Attempts':[],
                            'Rushing Yards':[],
                            'TD Rush':[],
                            'Rushing Fumble':[],
                            '2pt Rushing Conversion':[],
                            'Each Reception':[],
                            'Receiving Targets':[],
                            'Receiving Yards':[],
                            'TD Reception':[],
                            'Receiving Fumble':[],
                            '2pt Receiving Conversion':[],
                            'Each Sack':[],
                            'Interception Return TD':[],
                            'Fumble Return TD':[],
                            'Kickoff Return TD':[],
                            'Punt Return TD':[],
                            'Blocked Punt or FG return for TD':[],
                            'Blocked Punt, PAT or FG':[],
                            'Each Interception':[],
                            'Each Fumble Recovered':[],
                            'Each Safety':[],
                            '0 points allowed':[],
                            '1-6 points allowed':[],
                            '7-13 points allowed':[],
                            '14-17 points allowed':[],
                            '28-34 points allowed':[],
                            '35-45 points allowed':[],
                            '46+ points allowed':[],
                            'Less than 100 total yards allowed':[],
                            '100-199 total yards allowed':[],
                            '200-299 yards allowed':[],
                            '350-399 yards allowed':[],
                            '400-449 yards allowed':[],
                            '450-499 yards allowed':[],
                            '500-549 yards allowed':[],
                            '550+ yards allowed':[],
                            '2pt Return':[],
                            '1pt Safety':[],
                            'Defense Fumbles Lost':[],
                            'Actual':[],
                            'Fumble Recovered for TD':[]
                            })
        box_score = league.box_scores(wk)
        player_wk=wk
        print(wk)
        if wk==15:
            matchups = 7
        else:
            matchups = 6
        for matchup in range(matchups):
            for i in ['home','away']:
                wrNum = 1
                rbNum = 1
                beNum = 1
                for player in range(17):
                    if box_score[matchup].away_team==0:
                        pass
                    else:
                        empty=0
                        if i =='home':
                            try:
                                player_name_home = box_score[matchup].home_lineup[player].name
                                # print(player_name_home, player_wk)
                                player_id = box_score[matchup].home_lineup[player].playerId
                                plyr = box_score[matchup].home_lineup[player]
                                team = box_score[matchup].home_team.team_name
                                bye = box_score[matchup].home_lineup[player].on_bye_week
                                status = box_score[matchup].home_lineup[player].active_status
                                pos = plyr.position
                                player_key = str(player_wk)+player_name_home
                                home='1'
                                slotTemp = box_score[matchup].home_lineup[player].lineupSlot
                                if slotTemp == 'RB/WR/TE':
                                    slot = 'Flex'
                                elif slotTemp == 'RB':
                                    slot = slotTemp+str(rbNum)
                                    rbNum+=1
                                elif slotTemp == 'WR':
                                    slot = slotTemp+str(wrNum)
                                    wrNum+=1
                                elif slotTemp == 'BE':
                                    slot = slotTemp+str(beNum)
                                    beNum+=1
                                else:
                                    slot = slotTemp
                                if pos != 'D/ST':
                                    headshot = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/"+str(player_id)+".png&w=96&h=70&cb=1"
                                else:
                                    headshot = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/"+plyr.proTeam.lower()+".png&h=50&w=50"
                                # if player_id==8439:
                                    # print("loop1", player_name_home, plyr, team, bye, status)
                            except IndexError:
                                empty=1
                                # print('empty1')
                        else:
                            try:
                                player_name_home = box_score[matchup].away_lineup[player].name
                                # print(player_name_home, player_wk)
                                player_id = box_score[matchup].away_lineup[player].playerId
                                plyr = box_score[matchup].away_lineup[player]
                                team = box_score[matchup].away_team.team_name
                                bye = box_score[matchup].away_lineup[player].on_bye_week
                                status = box_score[matchup].away_lineup[player].active_status
                                pos = plyr.position
                                player_key = str(player_wk)+player_name_home
                                home='0'
                                slotTemp = box_score[matchup].away_lineup[player].lineupSlot
                                if slotTemp == 'RB/WR/TE':
                                    slot = 'Flex'
                                elif slotTemp == 'RB':
                                    slot = slotTemp+str(rbNum)
                                    rbNum+=1
                                elif slotTemp == 'WR':
                                    slot = slotTemp+str(wrNum)
                                    wrNum+=1
                                elif slotTemp == 'BE':
                                    slot = slotTemp+str(beNum)
                                    beNum+=1
                                else:
                                    slot = slotTemp
                                if pos != 'D/ST':
                                    headshot = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/"+str(player_id)+".png&w=96&h=70&cb=1"
                                else:
                                    headshot = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/"+plyr.proTeam.lower()+".png&h=50&w=50"
                                # if player_id==8439:
                                    # print("loop2", player_name_home, plyr, team, bye, status)
                            except IndexError:
                                empty=1
                                # print('empty2')
                        qb,rb,other = '','',''
                        if pos=='QB':
                            qb,rb,other='lostFumbles','junk','junk'
                        elif pos=='RB':
                            qb,rb,other='junk','lostFumbles','junk'
                        else:
                            qb,rb,other='junk','junk','lostFumbles'
                        temp = []
                        stats = [
                        'madeExtraPoints',
                        'attemptedExtraPoints',
                        'madeFieldGoalsFromUnder40',
                        'madeFieldGoalsFrom40To49',
                        'madeFieldGoalsFrom50Plus',
                        'madeFieldGoalsFrom60Plus',
                        # 'madeFieldGoals',
                        'attemptedFieldGoals',
                        'passingCompletions',
                        'passingAttempts',
                        'passingYards',
                        'passingTouchdowns',
                        'passingInterceptions',
                        qb,
                        'passing2PtConversions',
                        'rushingAttempts',
                        'rushingYards',
                        'rushingTouchdowns',
                        rb,
                        'rushing2PtConversions',
                        'receivingReceptions',
                        'receivingTargets',
                        'receivingYards',
                        'receivingTouchdowns',
                        other,
                        'receiving2PtConversions',
                        'defensiveSacks',
                        'interceptionReturnTouchdowns',
                        'fumbleReturnTouchdowns',
                        'kickoffReturnTouchdowns',
                        'puntReturnTouchdowns',
                        'defensiveBlockedKickForTouchdowns',
                        'defensiveBlockedKicks',
                        'defensiveInterceptions',
                        'defensiveFumbles',
                        'defensiveSafeties',
                        'defensive0PointsAllowed',
                        'defensive1To6PointsAllowed',
                        'defensive7To13PointsAllowed',
                        'defensive14To17PointsAllowed',
                        'defensive28To34PointsAllowed',
                        'defensive35To45PointsAllowed',
                        'defensive45PlusPointsAllowed',
                        'defensiveLessThan100YardsAllowed',
                        'defensive100To199YardsAllowed',
                        'defensive200To299YardsAllowed',
                        # 'defensive300To349YardsAllowed',
                        'defensive350To399YardsAllowed',
                        'defensive400To449YardsAllowed',
                        'defensive450To499YardsAllowed',
                        'defensive500To549YardsAllowed',
                        'defensive550PlusYardsAllowed',
                        # '2pt Return':[],
                        'junk',
                        'junk', #1pt safety
                        'junk' #'defensiveFumbles'/,
                        ,'fumbleRecoveredForTD'
                        ]
                        if (not(bye) and status!='bye' and empty==0): ## or (player_id==8439 and player_wk!=12) or (player_id==3116593 and player_wk!=7) or (player_id==3051392 and player_wk!=7) or (player_id==2980453 and player_wk!=12) or (player_id==3051926 and player_wk!=5)  or (player_id==2577327 and player_wk!=10) or (player_id==11122 and player_wk!=11) or (player_id==4241457 and player_wk!=9)  or (player_id==4360569 and player_wk!=9 and player_wk<=13)  or (player_id==4361579 and player_wk!=14) or (player_id==3912547 and player_wk!=6) or (player_id==2977187 and player_wk!=6) or (player_id==3051876 and player_wk!=12) or (player_id==3126486 and player_wk!=9):
                            for item in stats:
                                try:
                                    # print(plyr.name, item, player_wk)
                                    value=plyr.points_breakdown[item]
                                    # if player_id==8439:
                                        # print("try2", player_name_home, item, value)

                                except KeyError:
                                    value=0
                                    # if player_id==8439:
                                        # print("keyerror2", player_name_home, item, value)
                                temp.append(value)
                                # if player_id==8439:
                                    # print("loop3", player_name_home, plyr, team, bye, status)
                            player_row_home = pd.DataFrame({
                                'Week':[player_wk],
                                'FantasyTeam':[team],
                                'Player Name':[player_name_home],
                                'PlayerID':[player_id],
                                'Headshot_url':[headshot],
                                'NFL_Team':[plyr.proTeam],
                                'Status':[plyr.active_status],
                                'Opponent':[plyr.pro_opponent],
                                'Position':[plyr.position],
                                'PositionRank':[plyr.posRank],
                                'Lineup Slot': [slot],
                                'PlayerKey':[player_key],
                                'Home':[home],
                                'Bye':[plyr.on_bye_week],
                                'Projected':[plyr.projected_points],
                                'Each PAT Made':temp[0],
                                'PAT Attempt':temp[1],
                                'FG Made (0-39 yards)':temp[2],
                                'FG Made (40-49 yards)':temp[3],
                                'FG Made (50-59 yards)':temp[4] - temp[5],
                                'FG Made (60+ yards)':temp[5],
                                'Field Goal Attempted':temp[6],
                                'Passes Caught':temp[7],
                                'Pass Attempts':temp[8],
                                'Passing Yards':temp[9],
                                'TD Pass':temp[10],
                                'Interceptions Thrown':temp[11],
                                'Passer Fumble':temp[12],
                                '2pt Passing Conversion':temp[13],
                                'Rushing Attempts':temp[14],
                                'Rushing Yards':temp[15],
                                'TD Rush':temp[16],
                                'Rushing Fumble':temp[17],
                                '2pt Rushing Conversion':temp[18],
                                'Each Reception':temp[19],
                                'Receiving Targets':temp[20],
                                'Receiving Yards':temp[21],
                                'TD Reception':temp[22],
                                'Receiving Fumble':temp[23],
                                '2pt Receiving Conversion':temp[24],
                                'Each Sack':temp[25],
                                'Interception Return TD':temp[26],
                                'Fumble Return TD':temp[27],
                                'Kickoff Return TD':temp[28],
                                'Punt Return TD':temp[29],
                                'Blocked Punt or FG return for TD':temp[30],
                                'Blocked Punt, PAT or FG':temp[31],
                                'Each Interception':temp[32],
                                'Each Fumble Recovered':temp[33],
                                'Each Safety':temp[34],
                                '0 points allowed':temp[35],
                                '1-6 points allowed':temp[36],
                                '7-13 points allowed':temp[37],
                                '14-17 points allowed':temp[38],
                                '28-34 points allowed':temp[39],
                                '35-45 points allowed':temp[40],
                                '46+ points allowed':temp[41],
                                'Less than 100 total yards allowed':temp[42],
                                '100-199 total yards allowed':temp[43],
                                '200-299 yards allowed':temp[44],
                                '350-399 yards allowed':temp[45],
                                '400-449 yards allowed':temp[46],
                                '450-499 yards allowed':temp[47],
                                '500-549 yards allowed':temp[48],
                                '550+ yards allowed':temp[49],
                                '2pt Return':0,
                                '1pt Safety':temp[51],
                                'Defense Fumbles Lost':temp[52],
                                'Actual':[plyr.points],
                                'Fumble Recovered for TD':temp[53]
                                })

                            player_df = pd.concat([player_df,player_row_home],ignore_index=True)
                        elif empty==1:
                            # print('emptyloop')
                            pass
                        else:
                        # print('zerosloop', player_id,bye, status, empty,not(bye), status!='bye', empty==0, not(bye) and status!='bye' and empty==0)
                            player_row_bye = pd.DataFrame({
                                'Week':[player_wk],
                                'FantasyTeam':[team],
                                'Player Name':[player_name_home],
                                'PlayerID':[player_id],
                                'Headshot_url':[headshot],
                                'NFL_Team':[plyr.proTeam],
                                'Status':[plyr.active_status],
                                'Opponent':[plyr.pro_opponent],
                                'Position':[plyr.position],
                                'PositionRank':[plyr.posRank],
                                'PlayerKey':[player_key],
                                'Lineup Slot': [slot],
                                'Home':'Bye',
                                'Bye':1,
                                'Projected':0,
                                'Each PAT Made':0,
                                'PAT Attempt':0,
                                'FG Made (0-39 yards)':0,
                                'FG Made (40-49 yards)':0,
                                'FG Made (50-50 yards)':0,
                                'FG Made (60+ yards)':0,
                                'Field Goal Attempted':0,
                                'Passes Caught':0,
                                'Pass Attempts':0,
                                'Passing Yards':0,
                                'TD Pass':0,
                                'Interceptions Thrown':0,
                                'Passer Fumble':0,
                                '2pt Passing Conversion':0,
                                'Rushing Attempts':0,
                                'Rushing Yards':0,
                                'TD Rush':0,
                                'Rushing Fumble':0,
                                '2pt Rushing Conversion':0,
                                'Each Reception':0,
                                'Receiving Targets':0,
                                'Receiving Yards':0,
                                'TD Reception':0,
                                'Receiving Fumble':0,
                                '2pt Receiving Conversion':0,
                                'Each Sack':0,
                                'Interception Return TD':0,
                                'Fumble Return TD':0,
                                'Kickoff Return TD':0,
                                'Punt Return TD':0,
                                'Blocked Punt or FG return for TD':0,
                                'Blocked Punt, PAT or FG':0,
                                'Each Interception':0,
                                'Each Fumble Recovered':0,
                                'Each Safety':0,
                                '0 points allowed':0,
                                '1-6 points allowed':0,
                                '7-13 points allowed':0,
                                '14-17 points allowed':0,
                                '28-34 points allowed':0,
                                '35-45 points allowed':0,
                                '46+ points allowed':0,
                                'Less than 100 total yards allowed':0,
                                '100-199 total yards allowed':0,
                                '200-299 yards allowed':0,
                                '350-399 yards allowed':0,
                                '400-449 yards allowed':0,
                                '450-499 yards allowed':0,
                                '500-549 yards allowed':0,
                                '550+ yards allowed':0,
                                '2pt Return':0,
                                '1pt Safety':0,
                                'Defense Fumbles Lost':0,
                                'Actual':0,
                                'Fumble Recovered for TD':0
                                })

                            player_df = pd.concat([player_df,player_row_bye],ignore_index=True)
                        empty=0


        player_df['100-199 yard receiving game'] = player_df['Receiving Yards'].map(hundredyardgame)
        player_df['100-199 yard rushing game'] = player_df['Rushing Yards'].map(hundredyardgame)
        player_df['300-399 yard passing game'] = player_df['Passing Yards'].map(threehundredyardpassinggame)
        player_df_new = pd.melt(player_df,id_vars=['Week','FantasyTeam','Player Name','PlayerID','Headshot_url','Status','NFL_Team','Opponent','Position','PositionRank','PlayerKey','Bye','Projected','Actual', 'Home', 'Lineup Slot'],var_name='Attribute',value_name='Value')
        player_df_final = pd.DataFrame(player_df_new)

        # player_df_final.to_excel('playerpointsnew.xlsx',sheet_name='Sheet1',index=False)

        ##### player stats data

        players_table = player_df_final[['Week','FantasyTeam','NFL_Team','Player Name','Status','Home','Lineup Slot','PlayerKey']].copy()

        players_table = players_table.drop_duplicates()

        players_table['MatchupKey'] = players_table.apply(lambda row: str(row['Week'])[0]+row['FantasyTeam'] if row['Week']<10 else str(row['Week'])[:2]+row['FantasyTeam'],axis=1)
        player_df_final.to_excel('playerpointsnewWk'+str(wk)+'.xlsx',sheet_name='Sheet1',index=False)
        players_table.to_excel('playerstableWk'+str(wk)+'.xlsx',sheet_name='Sheet1',index=False)