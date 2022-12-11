from datetime import datetime
from bs4 import BeautifulSoup
import requests

isUpcomingMatchesAvailable = False

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
    isUpcomingMatchesAvailable = True if len(matchesBox.find_all("table")) == 2 else False

    if not isUpcomingMatchesAvailable:
        return

    upcomingMatchesTableBodys = matchesBox.find_all("table")[0].find_all("tbody")
    
    count = 0
    for body in upcomingMatchesTableBodys:
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

            url = td[1].find_all("div", class_="team-flex")[1].find("span", class_="team-logo-container").find("img")["src"]
            
            if (len(date) == 10):
                remaining = datetime.strptime(date, dateformat) - now
                remaining = str(remaining.days)
                timeformat = " days"
            else:
                dateHour = int(date.split(":")[0])
                nowHour = int(datetime.now().strftime("%H"))
                isDateToday = dateHour > nowHour

                if isDateToday:
                    remaining = dateHour - nowHour
                else:
                    remaining = str(24 - nowHour + dateHour)
                
                timeformat = " hours"

            upcomingMatches.append({
                "date": date,
                "remaining": str(remaining) + timeformat,
                "enemy": enemy,
                "image-url": url
            })

            count += 1


def previousMatchesData(previousMatches):
    matchesBox = doc_matches.find("div", id="matchesBox")
    # if upcoming matches are displayed, provious matches are in the second table. otherwise in the first
    prevMatchesIndex = 1 if len(matchesBox.find_all("table")) == 2 else 0
    previousMatchesTableBodys = matchesBox.find_all("table")[prevMatchesIndex].find_all("tbody")
   
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
            url = td[1].find_all("div", class_="team-flex")[1].find("span", class_="team-logo-container").find("img")["src"]

            previousMatches.append({
                "date": date,
                "score": score,
                "enemy": enemy,
                "image-url": url
            })

            countX += 1