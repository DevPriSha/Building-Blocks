#import stuff
import random
import time
import json
import requests

#DB module
try:
    import main
except:
    print("Could not import DB modules")

#flask modules
from flask import Flask, render_template, request, session
from flask_session import Session

#question files
import easy
#import medium
#import hard

def getHonor(CWID):
    req_stats = requests.get("https://www.codewars.com/api/v1/users/"+CWID).text
    userData = json.loads(req_stats)
    honor = userData["honor"]
    return honor

def checkques(quesAssigned, difficulty, CWID):
    quescompleted = json.loads(requests.get("https://www.codewars.com/api/v1/users/"+CWID+"/code-challenges/completed?page=0").text)
    for ques in quescompleted["data"]:
        quesURL = 'https://www.codewars.com/kata/'+ques["id"]+'/train/'
        print("quesassigned:", quesAssigned)
        print("quesURL:", quesURL)
        if quesURL == quesAssigned:
            try:
                height = main.get_height(CWID)
            except:
                print("Could not fetch height")
            height+= int(difficulty)
            isSolved = True
            try:
                main.insert_QuestionSolved(CWID,quesAssigned,isSolved)
                main.update_height(height,CWID)
            except:
                print("Could not update question status")
            return str(height)
        else:
            isSolved = False
            try:
                main.insert_QuestionSolved(CWID,quesAssigned,isSolved)
            except:
                print("Could not update question status")
    return "Quesno"

def quescheck(quesAssigned, difficulty,CWID):
    print(quesAssigned)
    result = checkques(quesAssigned, difficulty,CWID)
    print("height =" ,result)
    return result

def uniqueques(dictques, CWID):
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
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/instructions/', methods=['GET', 'POST'])
def instructions():
    return render_template("instructions.html")

@app.route('/thankyou/', methods=['GET', 'POST'])
def thankyou():
    CWID = session.get("ID")
    try:
        starttime = main.get_startTime(CWID)
        start_time = float(starttime)
        end_time = time.time()
        total_time = end_time - start_time
        main.update_time(total_time,CWID)
    except:
        print("Could not update time")
    return render_template("thankyou.html")



@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        player_name = request.form.get('participantname')
        player_id = request.form.get('participantid')
        name = player_name
        CWID = player_id
        session["ID"]=CWID
        session["NAME"]=name
        userlink = "https://www.codewars.com/users/"+CWID+"/completed"
        res = requests.get(userlink)
        if res.status_code != 200:
            print("True")
            return render_template("form.html", message = "Enter a valid CodeWars ID")
        else:
            print("Valid ID")
            try:
                main.insert_GameInfo(player_id,player_name)
                main.update_height(0,CWID)
                start_time = time.time()
                main.update_StartTime(start_time,CWID)
            except:
                print("Not updated to DBMS")
                pass
            return render_template("gamepage.html")
    return render_template("form.html", message = "")

#----------------------------------------------------------------------


@app.route('/assignques/', methods=['GET', 'POST'])
def assignques():
    CWID = session.get("ID")
    difficulty = int(request.args.get('difficulty'))
    print(difficulty)
    easy_ques = easy.easy_dict
    medium_ques = easy.easy_dict
    hard_ques = easy.easy_dict
    if difficulty == 1:
        quesAssigned = uniqueques(easy_ques, CWID)
    elif difficulty == 3:
        quesAssigned = uniqueques(medium_ques, CWID)
    elif difficulty == 5:
        quesAssigned = uniqueques(hard_ques, CWID)
    else:
        print("INVALID DIFFICULTY")

    return quesAssigned

@app.route('/scrapeScore/', methods=['GET', 'POST'])
def scrapeScore():
    CWID = session.get("ID")
    quesLink = request.args.get("quesgiven")
    difficulty = request.args.get("difficulty")
    oghonor = getHonor(CWID)
    time.sleep(5)
    newHonor = getHonor(CWID)
    while(oghonor == newHonor):
        time.sleep(5)
        newHonor = getHonor(CWID)
        print(newHonor)
    else:
        return quescheck(quesLink, difficulty, CWID)

if __name__ == "__main__":
    app.run(debug=True)
