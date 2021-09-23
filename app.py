#import stuff
import random
import re
import time
import json
import main

import requests
import psycopg2
from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template, request, url_for

import easy

#global variables
CWID = ""
height = 0
start_time = 0
end_time = 0

def getHonor():
    global CWID
    req_stats = requests.get("https://www.codewars.com/api/v1/users/"+CWID).text
    userData = json.loads(req_stats)
    honor = userData["honor"]
    return honor

def checkques(quesAssigned, difficulty):
    quescompleted = json.loads(requests.get("https://www.codewars.com/api/v1/users/"+CWID+"/code-challenges/completed?page=0").text)
    for ques in quescompleted["data"]:
        quesURL = 'https://www.codewars.com/kata/'+ques["id"]+'/train/'
        print("quesassigned:", quesAssigned)
        print("quesURL:", quesURL)
        if quesURL == quesAssigned:
            height = main.get_height(CWID)
            height+= int(difficulty)
            isSolved = True
            main.insert_QuestionSolved(CWID,quesAssigned,isSolved)
            main.update_height(height,CWID)
            return str(height)
        else:
            isSolved = False
            main.insert_QuestionSolved(CWID,quesAssigned,isSolved)
    return "Quesno"

def quescheck(quesAssigned, difficulty):
    print(quesAssigned)
    result = checkques(quesAssigned, difficulty)
    print("height =" ,result)
    return result

def uniqueques(dictques):
    global CWID
    completequesuser = json.loads(requests.get("https://www.codewars.com/api/v1/users/"+CWID+"/code-challenges/completed?page=0").text)
    while True:
        quesAssigned = random.choice(list(dictques.keys()))
        for ques in completequesuser["data"]:
            quesURL = 'https://www.codewars.com/kata/'+ques["id"]+'/train/'
            if quesAssigned == quesURL:
                break
        else:
            print(quesAssigned)
            return quesAssigned



#-----------------------------------------------------------------

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
    global CWID
    starttime = main.get_startTime(CWID)
    start_time = float(starttime)
    end_time = time.time()
    total_time = end_time - start_time
    main.update_time(total_time,CWID)
    return render_template("thankyou.html")



@app.route('/getplayerinfo', methods=['GET', 'POST'])
def playerinfo():
    player_name = request.args.get('player_name')
    player_id = request.args.get('player_id')
    name = player_name
    global CWID
    CWID = player_id
    userlink = "https://www.codewars.com/users/"+CWID+"/completed"
    res = requests.get(userlink)
    if res.status_code != 200:
        print("True")
        return "True"
    else:
        print("Valid ID")
    main.insert_GameInfo(player_id,player_name)
    main.update_height(0,CWID)
    start_time = time.time()
    main.update_StartTime(start_time,CWID)
    return redirect(url_for('gamepage'))

#----------------------------------------------------------------------

@app.route('/gamepage/', methods=['GET', 'POST'])
def gamepage():
    return render_template("gamepage.html")

@app.route('/assignques/', methods=['GET', 'POST'])
def assignques():
    difficulty = int(request.args.get('difficulty'))
    print(difficulty)
    easy_ques = easy.easy_dict
    medium_ques = easy.easy_dict
    hard_ques = easy.easy_dict
    if difficulty == 1:
        quesAssigned = uniqueques(easy_ques)
    elif difficulty == 3:
        quesAssigned = uniqueques(medium_ques)
    elif difficulty == 5:
        quesAssigned = uniqueques(hard_ques)
    else:
        print("INVALID DIFFICULTY")

    return quesAssigned

@app.route('/scrapeScore/', methods=['GET', 'POST'])
def scrapeScore():
    quesLink = request.args.get("quesgiven")
    difficulty = request.args.get("difficulty")
    oghonor = getHonor()
    time.sleep(15)
    newHonor = getHonor()
    while(oghonor == newHonor):
        time.sleep(15)
        newHonor = getHonor()
        print(newHonor)
    else:
        return quescheck(quesLink, difficulty)


#while rank does not change, keep doing scrapeScore
#else call quescheck()

if __name__ == "__main__":
    app.run(debug=True)
