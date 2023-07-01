import Data
import json
import os
import datetime

[name, ranking, top30, coach] = Data.mainPageData()
[winstreak, winrate, upcomingMatches, previousMatches] = Data.matchesPageData()

team = {
    "date": datetime.datetime.now().strftime("%d.%m - %H:%M"),
    "name": name,
    "ranking": ranking,
    "top30": top30,
    "coach": coach,
    "winstreak": winstreak,
    "winrate": winrate,
    "upcomingMatches": upcomingMatches,
    "previousMatches": previousMatches
}

with open(os.path.expanduser("~") + "/.config/hltvdata.json", "w", encoding="utf-8") as f:
    json.dump(team, f, ensure_ascii=False, indent=2)