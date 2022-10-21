import Data
import json
import os

upcomingMatches = []
previousMatches = []

[name, ranking, top30, avgage] = Data.mainPageData()
[winstreak, winrate] = Data.matchesPageData()
Data.upcomingMatchesData(upcomingMatches=upcomingMatches)
Data.previousMatchesData(previousMatches=previousMatches)

team = {
    "name": name,
    "ranking": ranking,
    "top30": top30,
    "avgage": avgage,
    "winstreak": winstreak,
    "winrate": winrate,
    "upcomingMatches": upcomingMatches,
    "previousMatches": previousMatches
}

with open(os.path.expanduser("~") + "/.config/hltvdata.json", "w", encoding="utf-8") as f:
    json.dump(team, f, ensure_ascii=False, indent=2)