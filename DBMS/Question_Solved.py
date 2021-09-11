import psycopg2
from connect_step1 import config

def insert(info_list):
    command = "INSERT INTO question_solved(codewarsid,question_name,solved_or_not) VALUES(%s,%s,%s);"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)
        conn.commit()
        cur.close()
    except (Exceptio,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        


