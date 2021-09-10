#import stuff
from flask import Flask, render_template, request
import psycopg2
import BeautifulSoup as bs4
import requests
import time

#global variables
CWID = ""
height = 0
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/form', methods=['GET', 'POST'])
#fetch input from flask and perform check on ID
def playerinfo():
    global CWID
    CWID = "DevPriSha" #to be fetched from flask (form.html)
    userlink = "https://www.codewars.com/users/"+CWID+"/completed"
    res = requests.get(userlink)
    if res.status_code != 200:
        #TODO return exception
        return render_template("form.html")
    #TODO add data to sql
    global height
    height = 0

@app.route('/gamepage', methods=['GET', 'POST'])
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
 


