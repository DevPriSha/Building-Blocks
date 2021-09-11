#import stuff
from flask import Flask, render_template, request, redirect, url_for
#import psycopg2
from bs4 import BeautifulSoup as bs
import requests
import time
import re
import easy 
import random

#global variables
CWID = ""
height = 0
start_time = 0
end_time = 0

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
    global start_time
    global end_time
    end_time = time.time()
    total_time = end_time - start_time
    #add total_time to DB
    return render_template("../thankyou.html") #DOES NOT WORK



@app.route('/getplayerinfo', methods=['GET', 'POST'])
def playerinfo():
    player_name = request.args.get('player_name')
    player_id = request.args.get('player_id')
    name = player_name #add this to DB
    global CWID
    CWID = player_id
    userlink = "https://www.codewars.com/users/"+CWID+"/completed"
    res = requests.get(userlink)
    if res.status_code != 200:
        print("True")
        return "True"
    else:
        print("Valid ID")
    #TODO add data to sql (name and CWID)
    global height
    height = 0
    global start_time
    start_time = time.time()
    return redirect(url_for('gamepage'))

#----------------------------------------------------------------------

@app.route('/gamepage/', methods=['GET', 'POST'])
def gamepage():
    return render_template("gamepage.html")

@app.route('/assignques/', methods=['GET', 'POST'])
def assignques():
    difficulty = int(request.args.get('difficulty'))
    easy_ques = easy.easy_dict
    medium_ques = {}
    hard_ques = {}
    if difficulty == 1:
        quesAssigned = random.choice(list(easy_ques.values()))
    elif difficulty == 3:
        quesAssigned = random.choice(medium_ques)
    elif difficulty == 5:
        quesAssigned = random.choice(hard_ques)
    else:
        print("INVALID DIFFICULTY")
    
    #TODO add check that same user does not get same ques
    #add quesAssigned to DB

    return quesAssigned

@app.route('/scrapeScore/', methods=['GET', 'POST'])
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

@app.route('/quescheck/', methods=['GET', 'POST'])
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


