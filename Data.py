from datetime import datetime
from bs4 import BeautifulSoup
import requests

dateformat = "%d/%m/%Y"
now = datetime.now()

url_main = "https://www.hltv.org/team/5973/liquid#tab-infoBox"
res_main = requests.get(url_main)

doc_main = BeautifulSoup(res_main.text, "html.parser")
def mainPageData():
    profileTeamStats = doc_main.find_all("div", class_="profile-team-stat")

    name = doc_main.find("h1", class_="profile-team-name").text
    ranking = profileTeamStats[0].find("span").find("a").text
    top30 = profileTeamStats[1].find("span").text
    avgage = profileTeamStats[2].find("span").text

    return [name, ranking, top30, avgage]


url_matches = url_main + "#tab-matchesBox"
res_matches = requests.get(url_matches)
doc_matches = BeautifulSoup(res_matches.text, "html.parser")


def matchesPageData():
    matchesBox = doc_matches.find("div", id="matchesBox")

    winstreak = matchesBox.find("div", class_="highlighted-stats-box").find("div", class_="highlighted-stat").find("div").text
    winrate = matchesBox.find("div", class_="highlighted-stats-box").find_all("div", class_="highlighted-stat")[1].find("div").text

    return [winstreak, winrate]


def upcomingMatchesData(upcomingMatches):
    matchesBox = doc_matches.find("div", id="matchesBox")
    previousMatchesTableBodys = matchesBox.find_all("table")[0].find_all("tbody")
    
    count = 0
    for body in previousMatchesTableBodys:
        if count == 5: return

        trs = body.find_all("tr", class_="team-row")
        for tr in trs:
            if count == 5: return

            td = tr.find_all("td")

            date = td[0].find("span").text
            if len(td[1].find_all("div", class_="team-flex")[1].find_all("a")) == 0:
                enemy = td[1].find_all("div", class_="team-flex")[1].find("span", class_="team-name").text
            else:
                enemy = td[1].find_all("div", class_="team-flex")[1].find_all("a")[1].text
            
            remaining = datetime.strptime(date, dateformat) - now

            upcomingMatches.append({
                "date": date,
                "remaining": "in " + str(remaining.days) + " days",
                "enemy": enemy,
            })

            count += 1


def previousMatchesData(previousMatches):
    matchesBox = doc_matches.find("div", id="matchesBox")
    previousMatchesTableBodys = matchesBox.find_all("table")[1].find_all("tbody")
   
    countX = 0
    for body in previousMatchesTableBodys:
        if countX == 5: return

        trs = body.find_all("tr", class_="team-row")
        for tr in trs:
            if countX == 5: return

            td = tr.find_all("td")

            date = td[0].find("span").text
            scoreCell = td[1].find("div", class_="score-cell").find_all("span")
            score = scoreCell[0].text + ":" + scoreCell[2].text
            enemy = td[1].find_all("div", class_="team-flex")[1].find_all("a")[1].text

            previousMatches.append({
                "date": date,
                "score": score,
                "enemy": enemy,
            })

            countX += 1