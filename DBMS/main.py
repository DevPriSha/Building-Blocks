import Game_Info
import Question_Solved

def insert_GameInfo(id,name):
    Game_Info.insert([id,name])

def get_question():
    pass

def insert_QuestionSolved(id,question_name,solved):
    Question_Solved.insert([id,question_name,solved])

def update_time(time,id):
    Game_Info.update_time([time,id])

def update_height(height,id):
    Game_Info.update_height([height,id])

def get_height(id):
    height = Game_Info.get_height([id])
    return height

def get_time(time):
    time = Game_Info([time])
    return time


