from espn_api.football import League
import pandas as pd
#import espnfantasyfootball as espn

league = League(league_id=801987389, year=2024, espn_s2='AEBcqdxIV%2Flb%2FIgTmPJYzV0cH8ez7YE6t8hWYzunjHzgOhlDJwWGH9amwY4Uny7Nf8dq47ZDWhns7WsN1FsDa7zQODG%2Bd%2FOGEPv2ojYfp9sTRzvZA0tk3xunHPP65PpzT2NtpgKRVVRpv%2F21ippabE3Tfs3ojNs83YnVvOWGUefVFQ4ZFn5yoSIguR3ySPAWxkmWy72kv0hvaFdpdXxdx%2BIE9AQ%2BnzOunbQxE1bfiiqi2d4McVcEfZjDVOxtXUDu54n2tperpJAU2t0DT2x4gUrJ', swid='{7A925BC0-142F-4FE0-925B-C0142FFFE09F}')


# print(league.standings_weekly(1))
# print(league.scoreboard(5))
# print(league.teams)
team = league.teams[6]
standing = team.stats
# print(league.standings_weekly(1))
# print(team)
# print(team.roster)
# print(league.power_rankings(week=13))
# print(team.roster[0].stats)
# print(league.load_roster_week(7))

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

standings_df = pd.DataFrame({'Team':[],'Week':[],'Leage_Rank':[],'Division_Rank':[]})
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
        new_row = pd.DataFrame({'Team':[team],'Week':[week],'Leage_Rank':[league_ranking],'Division_Rank':[div_standing]})
        standings_df = pd.concat([standings_df,new_row],ignore_index=True)

# print(standings_df)
# standings_df.to_excel('standings.xlsx', sheet_name='Sheet1', index=False)
















# league = espn.FantasyLeague(league_id=801987389, 
#                             year=2024, 
#                             espn_s2='AEBcqdxIV%2Flb%2FIgTmPJYzV0cH8ez7YE6t8hWYzunjHzgOhlDJwWGH9amwY4Uny7Nf8dq47ZDWhns7WsN1FsDa7zQODG%2Bd%2FOGEPv2ojYfp9sTRzvZA0tk3xunHPP65PpzT2NtpgKRVVRpv%2F21ippabE3Tfs3ojNs83YnVvOWGUefVFQ4ZFn5yoSIguR3ySPAWxkmWy72kv0hvaFdpdXxdx%2BIE9AQ%2BnzOunbQxE1bfiiqi2d4McVcEfZjDVOxtXUDu54n2tperpJAU2t0DT2x4gUrJ', 
#                             swid='{7A925BC0-142F-4FE0-925B-C0142FFFE09F}')

# league.get_matchup_data
# league.get_league_data


