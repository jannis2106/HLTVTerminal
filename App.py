import Data
import json

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

# print(team)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(team, f, ensure_ascii=False, indent=2)

# print(previousMatches)

# print(name)
# print(ranking + "    Winstreak: " + winstreak + "    WR: " + winrate + "    top30: " + top30 + "    avg age: " + avgage)

# print("---------------------------------------------------------------------------------------------------------")
# print(previousMatches[0]["enemy"] + "\t\t" + previousMatches[1]["enemy"] + "\t\t" + previousMatches[2]["enemy"] + "\t\t" + previousMatches[3]["enemy"] + "\t\t" + previousMatches[4]["enemy"])
# print(previousMatches[0]["score"] + "\t\t" + previousMatches[1]["score"] + "\t\t" + previousMatches[2]["score"] + "\t\t" + previousMatches[3]["score"] + "\t\t\t" + previousMatches[4]["score"])
# print("---------------------------------------------------------------------------------------------------------")
# print(upcomingMatches[0]["enemy"] + "\t\t" + upcomingMatches[1]["enemy"] + "\t\t" + upcomingMatches[2]["enemy"] + "\t\t" + upcomingMatches[3]["enemy"] + "\t\t" + upcomingMatches[4]["enemy"])
# print(upcomingMatches[0]["date"] + "\t\t" + upcomingMatches[1]["date"] + "\t\t" + upcomingMatches[2]["date"] + "\t\t" + upcomingMatches[3]["date"] + "\t\t\t" + upcomingMatches[4]["date"])
