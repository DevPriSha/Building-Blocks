#import stuff
from flask import Flask, render_template, request
#import psycopg2
from bs4 import BeautifulSoup as bs
import requests
import time
import re

#global variables
CWID = ""
height = 0

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/form/', methods=['GET', 'POST'])
def form():
    return render_template("form.html")

@app.route('/instructions/', methods=['GET', 'POST'])
def instructions():
    return render_template("instructions.html")

@app.route('/thankyou/', methods=['GET', 'POST'])
def thankyou():
    return render_template("thankyou.html")



@app.route('/getplayerinfo', methods=['GET', 'POST'])
def playerinfo(player_name, player_id):
    name = player_name #add this to DB
    global CWID
    CWID = player_id
    userlink = "https://www.codewars.com/users/"+CWID+"/completed"
    res = requests.get(userlink)
    if res.status_code != 200:
        return True
    #TODO add data to sql (name and CWID)
    global height
    height = 0
    return render_template("gamepage.html")

@app.route('/gamepage/', methods=['GET', 'POST'])
def gamepage():
    return render_template("gamepage.html")
def assignques(difficulty):
    pass #TODO assign question based on difficulty and return html statement to open ques in new tab

def scrapeScore():
    req_stats = requests.get("https://www.codewars.com/users/"+CWID+"/stats")
    stats_soup =  bs(req_stats.text, 'html.parser')
    stat_soup = stats_soup.find("div", attrs={"class": "px-4 pb-4"})
    rank = stat_soup.find("div", attrs={"class": "stat"}).text
    pattern = re.compile("\d+")
    rank = pattern.findall(rank)
    rank = int(rank[0])
    return rank

#while rank does not change, keep doing scrapeScore
#else call quescheck()


def quescheck(quesAssigned, difficulty):
    req_quest = requests.get("https://www.codewars.com/users/"+CWID+"/completed")
    kata = bs(req_quest.content)
    stat_ = kata.find("div", attrs={"class": "w-full md:w-8/12"})
    ques = stat_.find("a").text
    if ques == quesAssigned:
        global height
        height+= difficulty
        isSolved = True
        #update DB
    else:
        isSolved = False
        #update DB
        return
 
if __name__ == "__main__":
    app.run(debug=True)


