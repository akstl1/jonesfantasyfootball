from espn_api.football import League
import pandas as pd
#import espnfantasyfootball as espn

league = League(league_id=801987389, year=2024, espn_s2='AEBcqdxIV%2Flb%2FIgTmPJYzV0cH8ez7YE6t8hWYzunjHzgOhlDJwWGH9amwY4Uny7Nf8dq47ZDWhns7WsN1FsDa7zQODG%2Bd%2FOGEPv2ojYfp9sTRzvZA0tk3xunHPP65PpzT2NtpgKRVVRpv%2F21ippabE3Tfs3ojNs83YnVvOWGUefVFQ4ZFn5yoSIguR3ySPAWxkmWy72kv0hvaFdpdXxdx%2BIE9AQ%2BnzOunbQxE1bfiiqi2d4McVcEfZjDVOxtXUDu54n2tperpJAU2t0DT2x4gUrJ', swid='{7A925BC0-142F-4FE0-925B-C0142FFFE09F}')

# print(league.standings_weekly(1))
# print(league.scoreboard(5))
# print(league.teams)
# team = league.teams[6]
# print(team)
# print(team.roster)
# print(league.power_rankings(week=13))
# print(team.roster[0].stats)
# print(league.load_roster_week(7))

draft_df = pd.DataFrame({'Team':[],'Player':[],'Round':[],'Pick':[]})

for i in range(204):
    # print(player([league.draft[i].playerName]))
    new_row = pd.DataFrame({'Team':[league.draft[i].team.team_name],'Player':[league.draft[i].playerName],'Round':[league.draft[i].round_num],'Pick':[league.draft[i].round_pick]})
    draft_df = pd.concat([draft_df,new_row],ignore_index=True)


#draft_df.to_excel('draft.xlsx', sheet_name='Sheet1', index=False)



# league = espn.FantasyLeague(league_id=801987389, 
#                             year=2024, 
#                             espn_s2='AEBcqdxIV%2Flb%2FIgTmPJYzV0cH8ez7YE6t8hWYzunjHzgOhlDJwWGH9amwY4Uny7Nf8dq47ZDWhns7WsN1FsDa7zQODG%2Bd%2FOGEPv2ojYfp9sTRzvZA0tk3xunHPP65PpzT2NtpgKRVVRpv%2F21ippabE3Tfs3ojNs83YnVvOWGUefVFQ4ZFn5yoSIguR3ySPAWxkmWy72kv0hvaFdpdXxdx%2BIE9AQ%2BnzOunbQxE1bfiiqi2d4McVcEfZjDVOxtXUDu54n2tperpJAU2t0DT2x4gUrJ', 
#                             swid='{7A925BC0-142F-4FE0-925B-C0142FFFE09F}')

# league.get_matchup_data
# league.get_league_data


