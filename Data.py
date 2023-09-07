from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

isUpcomingMatchesAvailable = False
dateformat = "%d/%m/%Y"
now = datetime.now()
url_main = "https://www.hltv.org/team/5973/liquid#tab-infoBox"

def initDriver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(url)
    html = driver.page_source
    driver.quit()

    return html

def fetchMainPageDate(doc):
    profileTeamStats = doc.find_all("div", class_="profile-team-stat")

    name = doc.find("h1", class_="profile-team-name").text
    ranking = profileTeamStats[0].find("span").find("a").text
    top30 = profileTeamStats[1].find("span").text
    coach = profileTeamStats[3].find("span").text

    return [name, ranking, top30, coach]

def fetchMatchesPageData(doc):
    matchesBox = doc.find("div", id="matchesBox")

    winstreak = matchesBox.find("div", class_="highlighted-stats-box").find("div", class_="highlighted-stat").find("div").text
    winrate = matchesBox.find("div", class_="highlighted-stats-box").find_all("div", class_="highlighted-stat")[1].find("div").text

    return [winstreak, winrate]

def fetchUpcomingMatchesData(doc):
    matchesBox = doc.find("div", id="matchesBox")
    isUpcomingMatchesAvailable = True if len(matchesBox.find_all("table")) == 2 else False

    if not isUpcomingMatchesAvailable:
        return

    upcomingMatchesTableBodys = matchesBox.find_all("table")[0].find_all("tbody")
    
    upcomingMatches = []

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
                remaining = str(remaining.days + 1)
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

    return upcomingMatches

def fetchPreviousMatchesData(doc):
    matchesBox = doc.find("div", id="matchesBox")
    # if upcoming matches are displayed, provious matches are in the second table. otherwise in the first
    prevMatchesIndex = 1 if len(matchesBox.find_all("table")) == 2 else 0
    previousMatchesTableBodys = matchesBox.find_all("table")[prevMatchesIndex].find_all("tbody")

    previousMatches = []

    countX = 0
    for body in previousMatchesTableBodys:
        if countX == 5: break

        trs = body.find_all("tr", class_="team-row")
        for tr in trs:
            if countX == 5: break

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

    return previousMatches

def mainPageData():
    html = initDriver(url_main)
    doc = BeautifulSoup(html, "html.parser")

    return fetchMainPageDate(doc)

def matchesPageData():
    html = initDriver(url_main + "#tab-matchesBox")
    doc = BeautifulSoup(html, "html.parser")
    
    [winstreak, winrate] = fetchMatchesPageData(doc)
    upcomingMatches = fetchUpcomingMatchesData(doc)
    previousMatches = fetchPreviousMatchesData(doc)

    return [winstreak, winrate, upcomingMatches, previousMatches]
