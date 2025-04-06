from espn_api.football import League
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

league = League(league_id=os.getenv("LEAGUE_ID"), year=int(os.getenv("YEAR")), espn_s2=os.getenv("S2"),swid=os.getenv("SWID"))


# print(league.standings_weekly(1))
# standing = team.stats
# print(league.standings_weekly(1))
# print(team.roster[0].stats)
# print(league.load_roster_week(7))
# print(team.outcomes)



draft_df = pd.DataFrame({'Team':[],'Player':[],'Round':[],'Pick':[]})
#

for i in range(204):
    new_row = pd.DataFrame({'Team':[league.draft[i].team.team_name],'Player':[league.draft[i].playerName],'Round':[league.draft[i].round_num],'Pick':[league.draft[i].round_pick]})
    draft_df = pd.concat([draft_df,new_row],ignore_index=True)


#draft_df.to_excel('draft.xlsx', sheet_name='Sheet1', index=False)



##### power rankings data

power_ranking_df = pd.DataFrame({'Team':[],'Week':[],'Rank':[]})
for wk in range(1,18):
    rankings = league.power_rankings(week=wk)
    week=wk
    for rank in range(12):
        team = rankings[rank][1].team_name
        ranking = rank+1
        new_row = pd.DataFrame({'Team':[team],'Week':[week],'Rank':[ranking]})
        power_ranking_df = pd.concat([power_ranking_df,new_row],ignore_index=True)
        
# print(power_ranking_df)
# power_ranking_df.to_excel('power_ranking.xlsx', sheet_name='Sheet1', index=False)

# (league.power_rankings(week=13)[0][1].team_name)

##### standings data

standings_df = pd.DataFrame({'Team':[],'Week':[],'League_Rank':[],'Division_Rank':[]})
for wk in range(1,17):
    standings = league.standings_weekly(wk)
    week=wk
    travis = 1
    taylor = 1
    for rank in range(12):
        team = standings[rank].team_name
        league_ranking = rank+1
        if standings[rank].division_name=="Team Travis":
            div_standing = travis
            travis+=1
        else:
            div_standing = taylor
            taylor+=1
        new_row = pd.DataFrame({'Team':[team],'Week':[week],'League_Rank':[league_ranking],'Division_Rank':[div_standing]})
        standings_df = pd.concat([standings_df,new_row],ignore_index=True)

# print(standings_df)
# standings_df.to_excel('standings.xlsx', sheet_name='Sheet1', index=False)



##### matchup data

matchups_df = pd.DataFrame({'Team':[],
                            'Opponent':[],
                            'Week':[],
                            'Home_Or_Away':[],
                            'Projected_score':[],
                            'Actual_score':[],
                            'matchup_type':[],
                            'projected_variance':[],
                            'actual_variance':[],
                            'matchup_header':[],
                            'result':[]
                            })
for wk in range(1,19):
    box_score = league.box_scores(wk)
    week=wk
    for matchup in range(6):
        home_team = box_score[matchup].home_team
        home_projected = box_score[matchup].home_projected
        home_actual = box_score[matchup].home_score

        away_team = box_score[matchup].away_team
        if away_team==0:
            away_tm = 'Bye'
        else:
            away_tm = away_team.team_name
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
                            'Week':[week],
                            'Home_Or_Away':['Home'],
                            'Projected_score':[home_projected],
                            'Actual_score':[home_actual],
                            'matchup_type':[matchup_type],
                            'projected_variance':[home_projected-away_projected],
                            'actual_variance':[home_actual-away_actual],
                            'matchup_header':[header],
                            'result':[result_home]
                            })
        
        new_row_away = pd.DataFrame({
                            'Team':[away_tm],
                            'Opponent':[home_team.team_name],
                            'Week':[week],
                            'Home_Or_Away':['Away'],
                            'Projected_score':[away_projected],
                            'Actual_score':[away_actual],
                            'matchup_type':[matchup_type],
                            'projected_variance':[away_projected-home_projected],
                            'actual_variance':[away_actual-home_actual],
                            'matchup_header':[header],
                            'result':[result_away]
                            })
        new_row_home['projected_variance'] = new_row_home['projected_variance'].round(2)
        new_row_home['actual_variance'] = new_row_home['actual_variance'].round(2)

        new_row_away['projected_variance'] = new_row_away['projected_variance'].round(2)
        new_row_away['actual_variance'] = new_row_away['actual_variance'].round(2)

        matchups_df = pd.concat([matchups_df,new_row_home],ignore_index=True)
        matchups_df = pd.concat([matchups_df,new_row_away],ignore_index=True)

# matchups_df.to_excel('matchups.xlsx', sheet_name='Sheet1', index=False)

# print(matchups_df)

##### player stats data



player_df = pd.DataFrame({  'Week':[],
                            'FantasyTeam':[],
                            'Name':[],
                            'Status':[],
                            'Team':[],
                            'Opponent':[],
                            'Position':[],
                            'PositionRank':[],
                            'Bye':[],
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
                            '300-399 yards allowed':[],
                            '400-449 yards allowed':[],
                            '450-499 yards allowed':[],
                            '500-549 yards allowed':[],
                            '550+ yards allowed':[],
                            '2pt Return':[],
                            '1pt Safety':[],
                            'Defense Fumbles Lost':[],
                            'Actual':[]
                            })

# print(league.box_scores(17))
temp_player = league.box_scores(15)[2]
# print(temp_player.home_lineup)
# print(temp_player.home_lineup[0].name,temp_player.home_lineup[0].points_breakdown)
# print(temp_player.home_lineup[1].name,temp_player.home_lineup[1].points_breakdown)
# print(temp_player.home_lineup[2].name,temp_player.home_lineup[2].points_breakdown)
# print(temp_player.home_lineup[3].name,temp_player.home_lineup[3].points_breakdown)
# print(temp_player.home_lineup[4].name,temp_player.home_lineup[4].points_breakdown)
# print(temp_player.home_lineup[5].name,temp_player.home_lineup[5].points_breakdown)
# print(temp_player.home_lineup[6].name,temp_player.home_lineup[6].points_breakdown)
# print(temp_player.home_lineup[7].name,temp_player.home_lineup[7].points_breakdown)
# print(temp_player.home_lineup[8].name,temp_player.home_lineup[8].points_breakdown)
# print(temp_player.home_lineup[9].name,temp_player.home_lineup[9].points_breakdown)
# print(temp_player.home_lineup[10].name,temp_player.home_lineup[10].points_breakdown)
# print(temp_player.home_lineup[11].name,temp_player.home_lineup[11].points_breakdown)
# print(temp_player.home_lineup[12].name,temp_player.home_lineup[12].points_breakdown)
# print(temp_player.home_lineup[13].name,temp_player.home_lineup[13].points_breakdown)
# print(temp_player.home_lineup[14].name,temp_player.home_lineup[14].points_breakdown)
# print(temp_player.home_lineup[15].name,temp_player.home_lineup[15].points_breakdown)
# print(temp_player.home_lineup[16].name,temp_player.home_lineup[16].points_breakdown)
print(league.box_scores(5)[2].home_lineup[8].active_status)

# print(league.box_scores(13)[1].home_lineup[7].position)
# print(league.box_scores(13)[1].home_lineup[7].lineupSlot)
# print(league.box_scores(13)[1].home_lineup[7].active_status)
# print(league.box_scores(13)[1].home_lineup[7].on_bye_week)
# print(league.box_scores(13)[1].home_lineup[7].slot_position)
# print(league.box_scores(13)[1].home_lineup[7].pro_opponent)
# print(league.box_scores(13)[1].home_lineup[7].projected_points)
# print(league.box_scores(13)[1].home_lineup[7].proTeam)
# print(league.box_scores(13)[1].home_lineup[7].injuryStatus)
# print(league.box_scores(13)[1].home_lineup[7].injured)
# print(league.box_scores(13)[1].home_lineup[7].game_played)
# print(league.box_scores(14)[1].home_lineup[7].name)
# print(league.box_scores(14)[1].home_lineup[7].points)
# print(league.box_scores(14)[1].home_lineup[7].total_points)
# print(league.free_agents(week=1,position='D/ST',size=50))
# print(league.draft)
# print(league.box_scores(13)[1].home_lineup[0].points_breakdown['passingAttempts'])

for wk in range(1,18):
    box_score = league.box_scores(wk)
    player_wk=wk
    for matchup in range(6):
        for i in ['home','away']:
            for player in range(17):
                if box_score[matchup].away_team==0:
                    pass
                else:
                    empty=0
                    if i =='home':
                        try:
                            player_name_home = box_score[matchup].home_lineup[player].name
                            plyr = box_score[matchup].home_lineup[player]
                            team = box_score[matchup].home_team.team_name
                            bye = box_score[matchup].home_lineup[player].on_bye_week
                            status = box_score[matchup].home_lineup[player].active_status
                            pos = plyr.position
                        except IndexError:
                            empty=1
                    else:
                        try:
                            player_name_home = box_score[matchup].away_lineup[player].name
                            plyr = box_score[matchup].away_lineup[player]
                            team = box_score[matchup].away_team.team_name
                            bye = box_score[matchup].away_lineup[player].on_bye_week
                            status = box_score[matchup].away_lineup[player].active_status
                            pos = plyr.position
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
                        'madeFieldGoalsFrom50Plus',
                        'madeFieldGoalsFrom60Plus',
                        'madeFieldGoals',
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
                        'defensiveForcedFumbles',
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
                        'defensive300To349YardsAllowed',
                        'defensive350To399YardsAllowed',
                        'defensive400To449YardsAllowed',
                        'defensive450To499YardsAllowed',
                        'defensive500To549YardsAllowed',
                        'defensive550PlusYardsAllowed',
                        # '2pt Return':[],
                        'junk',
                        'defensiveSafeties',
                        'defensiveFumbles'
                        ]
                    if not(bye) and status!='bye' and empty==0:
                        for item in stats:
                            try:
                                # print(plyr.name, item, player_wk)
                                value=plyr.points_breakdown[item]

                            except KeyError:
                                value=[0]
                            temp.append(value)
                
                        player_row_home = pd.DataFrame({
                                'Week':[player_wk],
                                'FantasyTeam':[team],
                                'Name':[player_name_home],
                                'Team':[plyr.proTeam],
                                'Status':[plyr.active_status],
                                'Opponent':[plyr.pro_opponent],
                                'Position':[plyr.position],
                                'PositionRank':[plyr.posRank],
                                'Bye':[plyr.on_bye_week],
                                'Projected':[plyr.projected_points],
                                'Each PAT Made':temp[0],
                                'PAT Attempt':temp[1],
                                'FG Made (0-39 yards)':temp[2],
                                'FG Made (40-49 yards)':temp[3],
                                'FG Made (50-50 yards)':temp[4],
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
                                '300-399 yards allowed':temp[45],
                                '400-449 yards allowed':temp[46],
                                '450-499 yards allowed':temp[47],
                                '500-549 yards allowed':temp[48],
                                '550+ yards allowed':temp[49],
                                '2pt Return':0,
                                '1pt Safety':temp[51],
                                'Defense Fumbles Lost':temp[52],
                                'Actual':[plyr.points]
                                })

                        player_df = pd.concat([player_df,player_row_home],ignore_index=True)
                    elif empty==1:
                        pass
                    else:
                        temp2 = [0]*54
                        player_row_bye = pd.DataFrame({
                                'Week':[player_wk],
                                'FantasyTeam':[team],
                                'Name':[player_name_home],
                                'Team':[plyr.proTeam],
                                'Status':[plyr.active_status],
                                'Opponent':[plyr.pro_opponent],
                                'Position':[plyr.position],
                                'PositionRank':[plyr.posRank],
                                'Bye':1,
                                'Projected':0,
                                'Each PAT Made':temp2[0],
                                'PAT Attempt':temp2[1],
                                'FG Made (0-39 yards)':temp2[2],
                                'FG Made (40-49 yards)':temp2[3],
                                'FG Made (50-50 yards)':temp2[4],
                                'FG Made (60+ yards)':temp2[5],
                                'Field Goal Attempted':temp2[6],
                                'Passes Caught':temp2[7],
                                'Pass Attempts':temp2[8],
                                'Passing Yards':temp2[9],
                                'TD Pass':temp2[10],
                                'Interceptions Thrown':temp2[11],
                                'Passer Fumble':temp2[12],
                                '2pt Passing Conversion':temp2[13],
                                'Rushing Attempts':temp2[14],
                                'Rushing Yards':temp2[15],
                                'TD Rush':temp2[16],
                                'Rushing Fumble':temp2[17],
                                '2pt Rushing Conversion':temp2[18],
                                'Each Reception':temp2[19],
                                'Receiving Targets':temp2[20],
                                'Receiving Yards':temp2[21],
                                'TD Reception':temp2[22],
                                'Receiving Fumble':temp2[23],
                                '2pt Receiving Conversion':temp2[24],
                                'Each Sack':temp2[25],
                                'Interception Return TD':temp2[26],
                                'Fumble Return TD':temp2[27],
                                'Kickoff Return TD':temp2[28],
                                'Punt Return TD':temp2[29],
                                'Blocked Punt or FG return for TD':temp2[30],
                                'Blocked Punt, PAT or FG':temp2[31],
                                'Each Interception':temp2[32],
                                'Each Fumble Recovered':temp2[33],
                                'Each Safety':temp2[34],
                                '0 points allowed':temp2[35],
                                '1-6 points allowed':temp2[36],
                                '7-13 points allowed':temp2[37],
                                '14-17 points allowed':temp2[38],
                                '28-34 points allowed':temp2[39],
                                '35-45 points allowed':temp2[40],
                                '46+ points allowed':temp2[41],
                                'Less than 100 total yards allowed':temp2[42],
                                '100-199 total yards allowed':temp2[43],
                                '200-299 yards allowed':temp2[44],
                                '300-399 yards allowed':temp2[45],
                                '400-449 yards allowed':temp2[46],
                                '450-499 yards allowed':temp2[47],
                                '500-549 yards allowed':temp2[48],
                                '550+ yards allowed':temp2[49],
                                '2pt Return':0,
                                '1pt Safety':temp2[51],
                                'Defense Fumbles Lost':temp2[52],
                                'Actual':0
                                })

                        player_df = pd.concat([player_df,player_row_bye],ignore_index=True)
                    empty=0

# print(player_df)
player_df_new = pd.melt(player_df,id_vars=['Week','FantasyTeam','Name','Status','Team','Opponent','Position','PositionRank','Bye','Projected','Actual'],var_name='Stat',value_name='Val')
player_df_final = pd.DataFrame(player_df_new)
player_df_final.to_excel('playerpointsnew.xlsx',sheet_name='Sheet1',index=False)