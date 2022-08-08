import re
import csv 
from stats import *
 
def for_teams(stats, home, play_by_play, txt_posession):
    lst_away_sort = []
    lst_home_sort = []
    for i in range(len(stats)):
        check = stats[i]["Players\t"]
        
        for j in range(len(play_by_play)):
            name = re.search(r'(\w\. \w+)', play_by_play[j])
            foul = re.search(r'foul by \w\. \w+', play_by_play[j])
            if  name:
                name1 = name.group()
                if check == name1 and txt_posession[j] == home:
                    if (stats[i] not in lst_home_sort) and foul == None:
                        lst_home_sort.append(stats[i])
                elif check == name1 and txt_posession[j] != home:
                    if (stats[i] not in lst_away_sort) and foul == None:
                        lst_away_sort.append(stats[i])
    return [lst_away_sort, lst_home_sort]

def analysis_nba_game(play_by_play):
    with open(play_by_play, 'r') as csv_text:
        each_play = [each for each in (csv.reader(csv_text, delimiter = '|'))]
        txt_play = [each[-1] for each in each_play]
        txt_teams = [each[2] for each in each_play]
        txt_home = each_play[1][4]
        txt_away = each_play[1][3]
    func_stats(txt_play)
    lst_stats = func_stats(txt_play)
    teams = for_teams(lst_stats, txt_home, txt_play, txt_teams)
    lst_away_final = teams[0]
    lst_home_final = teams[1]
    dict_final = {"home_team": {"name":txt_home, "players_data": lst_home_final}, "away_team":{"name":txt_away, "players_data": lst_away_final}}

    print_nba_game_stats(lst_home_final)
    print("\n")
    print_nba_game_stats(lst_away_final)

def print_nba_game_stats(team_dict):
    headers = [keys for keys in team_dict[0].keys()]
    print(*headers, sep = "\t")
    for i in range(len(team_dict)):
        print(*team_dict[i].values(), sep = "\t")
    dict_total = {"Team Totals": 'Team Totals', "FG":0, "FGA":0, "FG%":0, "3P":0, "3PA":0, "3P%":0, "FT":0, "FTA":0, "FT%":0, "ORB":0, "DRB":0, "TRB":0, "AST":0, "STL":0, "BLK":0, "TOV":0, "PF":0, "PTS":0}
    for i in range(len(team_dict)):
        lst = [j for j in team_dict[i].keys()]
        for j in lst[1:]:
            dict_total[j] += team_dict[i][j]
            if dict_total["FG"] > 0 and dict_total["FGA"] > 0:
                dict_total["FG%"] = round((dict_total["FG"]/dict_total["FGA"]), 3)
    print(*dict_total.values(), sep = "\t")

analysis_nba_game("nba_game_warriors_thunder_20181016.txt")
