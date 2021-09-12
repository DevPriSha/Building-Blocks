import psycopg2
from connect_step1 import config
import random

def insert(info_list):
    command = "INSERT INTO question_bank(question_name,question_link,level) VALUES(%s,%s,%s);"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(command,info_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_question(info_list):
    command1 = "SELECT question_name from question_bank WHERE level=%s;"
    command2 = "SELECT question_name from question_solved WHERE codewarsid = %s AND question_bank.level = %s;"
    command3 = "SELECT question_link from question_bank WHERE question_name = %s;"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        question_chosen = "none"
        question_level_list = list(cur.execute(command1,info_list[1]))
        question_done_list = list(cur.execute(command2,info_list))
        question_list = list(set(question_level_list)-set(question_done_list))                                 
        question_chosen = random.choice(question_list)
        question_link = cur.execute(command3,question_chosen)

        conn.commit()
        cur.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return question_chosen
                    
                    
                            
ques = get_question(["hsdfgsd","hard"])
