from espn_api.football import League
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

league = League(league_id=os.getenv("LEAGUE_ID"), year=int(os.getenv("YEAR")), espn_s2=os.getenv("S2"),swid=os.getenv("SWID"))


# print(league.standings_weekly(1))
# print(league.scoreboard(5))
# print(league.teams)
# team = league.teams[6]
# standing = team.stats
# print(league.standings_weekly(1))
# print(team)
# print(team.roster)
# print(league.power_rankings(week=13))
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
# print(league.box_scores(13)[1].home_lineup[7].points_breakdown)
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
# print(league.box_scores(13)[1].home_lineup[7].name)
# print(league.box_scores(13)[1].home_lineup[0].points_breakdown['passingAttempts'])

for wk in range(1,3):
    box_score = league.box_scores(wk)
    player_wk=wk
    for matchup in range(6):
        for player in range(16):
            player_name_home = box_score[matchup].home_lineup[player].name

            player_row_home = pd.DataFrame({
                            'Week':[player_wk],
                            'FantasyTeam':[box_score[matchup].home_team.team_name],
                            'Name':[player_name_home],
                            'Team':[box_score[matchup].home_lineup[player].proTeam]
                            })

            player_df = pd.concat([player_df,player_row_home],ignore_index=True)

        for player in range(16):
            player_name_away = box_score[matchup].away_lineup[player].name
            player_row_away = pd.DataFrame({
                            'Week':[player_wk],
                            'FantasyTeam':[box_score[matchup].away_team.team_name],
                            'Name':[player_name_away],
                            'Team':[box_score[matchup].away_lineup[player].proTeam]
                            })
            player_df = pd.concat([player_df,player_row_away],ignore_index=True)

print(player_df)