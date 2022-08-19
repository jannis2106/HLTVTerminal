import json
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.console import Console
from rich import box

with open("data.json", "r", encoding="utf-8") as f:
    team = json.loads(f.read())

upcomingMatches = team["upcomingMatches"]
previousMatches = team["previousMatches"]

logo = """
         .-=*%@%*+-.           
   .:=*#@%*=@@@::=*#@%*=:.      
+#@%*++@@#  =@@  ++  .-=*%@#*   
@@@%:  :%@*  %@+@@=        *@.  
@%%@@%-  +@%%@@@@@+.       +@.  
@# .=#@@**@@@@@@@@@@%+     +@.  
@%+-:. +@@@@@@@@@@@##@:    +@.  
@@%%@@@@@@@@@@@%@@@@@@@.   *@.  
@#    @@@@@@@@@**@@@@@@@.  *@   
%@#%@@@@@@@@@@@% .-*@@@%@. %@   
+@#=::@@@@@@@@@@@+. *%+#= .@*   
.@%.-#@@@@@@@@@@@@@= .    #@:   
 :@@@%#@@@@@@@@@@@@@#:  .#@-    
  .*@*=@@@@@@@@@@@@@@@+*@#.     
    .=#@@@@@@@@@@@@@@@%+.       
        -+%@@@@@@@%*-.          
            :=*=:               """

layout = Layout()

# TABLES
# Upcoming Matches
upcomingMatchesTable = Table(box=box.SIMPLE_HEAD)
def genUpcomingMatchesTable():

    upcomingMatchesTable.add_column("Date")
    upcomingMatchesTable.add_column("Time Remaining")
    upcomingMatchesTable.add_column("Enemy")
    for game in upcomingMatches:
        upcomingMatchesTable.add_row(
            game["date"],
            game["remaining"],
            game["enemy"]
        )

# Previous Matches
previousMatchesTable = Table(box=box.SIMPLE_HEAD)
def genPreviousMatchesTable():

    previousMatchesTable.add_column("Date")
    previousMatchesTable.add_column("Game Score")
    previousMatchesTable.add_column("Enemy")
    for game in previousMatches:
        previousMatchesTable.add_row(
            game["date"],
            game["score"],
            game["enemy"]
        )

# PANELS
# Left Panel
logoPanel = Panel(
    logo,
    height=21,
    width=34
)

# Upper Panel
upperPanel = Panel(
    "Ranking: [bold]" + team["ranking"] + "[/bold]    Winstreak: [bold]" + team["winstreak"] + "[/bold]    Winrate: [bold]" + team["winrate"] + "[/bold]    Top 30: [bold]" + team["top30"] + "[/bold]    average age: [bold]" + team["avgage"] + "[/bold]",
)

#Matches Panels
upcomingMatchesPanel = Panel(
    upcomingMatchesTable,
    height=11
)

prevMatchesPanel = Panel(
    previousMatchesTable,
    height=11
)

# LAYOUTS
# Main Layout
layout.split_row(
    Layout(logoPanel, size=34),
    Layout(name="right", height=25)
)

# Right Layout
layout["right"].split_column(
    Layout(upperPanel, name="upper"),
    Layout(
        name="matches"
    )
)
layout["upper"].size = 3

# CONSOLE
console = Console()

# Make It Responsive
if console.width > 100:
    console.height = 21
else:
    console.height = 25

if console.width > 100:
    layout["matches"].split_row(
        prevMatchesPanel,
        upcomingMatchesPanel,
    )
else:
    layout["matches"].split_column(
        prevMatchesPanel,
        upcomingMatchesPanel,
    )


genPreviousMatchesTable()
genUpcomingMatchesTable()

console.print(layout)