from espn_api.football import League
import pandas as pd
#import espnfantasyfootball as espn

league = League(league_id=801987389, year=2024, espn_s2='AEBcqdxIV%2Flb%2FIgTmPJYzV0cH8ez7YE6t8hWYzunjHzgOhlDJwWGH9amwY4Uny7Nf8dq47ZDWhns7WsN1FsDa7zQODG%2Bd%2FOGEPv2ojYfp9sTRzvZA0tk3xunHPP65PpzT2NtpgKRVVRpv%2F21ippabE3Tfs3ojNs83YnVvOWGUefVFQ4ZFn5yoSIguR3ySPAWxkmWy72kv0hvaFdpdXxdx%2BIE9AQ%2BnzOunbQxE1bfiiqi2d4McVcEfZjDVOxtXUDu54n2tperpJAU2t0DT2x4gUrJ', swid='{7A925BC0-142F-4FE0-925B-C0142FFFE09F}')


# print(league.standings_weekly(1))
# print(league.scoreboard(5))
# print(league.teams)
team = league.teams[6]
# standing = team.stats
# print(league.standings_weekly(1))
# print(team)
print(team.roster)
# print(league.power_rankings(week=13))
# print(team.roster[0].stats)
# print(league.load_roster_week(7))
# print(team.outcomes)
# print(league.box_scores(15))

draft_df = pd.DataFrame({'Team':[],'Player':[],'Round':[],'Pick':[]})
#

for i in range(204):
    # print(player([league.draft[i].playerName]))
    new_row = pd.DataFrame({'Team':[league.draft[i].team.team_name],'Player':[league.draft[i].playerName],'Round':[league.draft[i].round_num],'Pick':[league.draft[i].round_pick]})
    draft_df = pd.concat([draft_df,new_row],ignore_index=True)


#draft_df.to_excel('draft.xlsx', sheet_name='Sheet1', index=False)



##### power rankings data

power_ranking_df = pd.DataFrame({'Team':[],'Week':[],'Rank':[]})
for wk in range(1,19):
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









# league = espn.FantasyLeague(league_id=801987389, 
#                             year=2024, 
#                             espn_s2='AEBcqdxIV%2Flb%2FIgTmPJYzV0cH8ez7YE6t8hWYzunjHzgOhlDJwWGH9amwY4Uny7Nf8dq47ZDWhns7WsN1FsDa7zQODG%2Bd%2FOGEPv2ojYfp9sTRzvZA0tk3xunHPP65PpzT2NtpgKRVVRpv%2F21ippabE3Tfs3ojNs83YnVvOWGUefVFQ4ZFn5yoSIguR3ySPAWxkmWy72kv0hvaFdpdXxdx%2BIE9AQ%2BnzOunbQxE1bfiiqi2d4McVcEfZjDVOxtXUDu54n2tperpJAU2t0DT2x4gUrJ', 
#                             swid='{7A925BC0-142F-4FE0-925B-C0142FFFE09F}')

# league.get_matchup_data
# league.get_league_data


