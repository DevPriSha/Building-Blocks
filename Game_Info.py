import psycopg2
from connect_step1 import config

def insert(id,name):

    command1 = "SELECT codewarsid FROM game_info WHERE codewarsid=%s;"
    command2 = "INSERT INTO game_info(codewarsid,name) VALUES(%s,%s);"
    command3 = "UPDATE game_info SET name=%s WHERE codewarsid=%s;"

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(command1,[id])
        codewarsid = cur.fetchone()
        if(codewarsid == None):
            cur.execute(command2,[id,name])
        else:
            cur.execute(command3,[name,id])

        conn.commit()
        cur.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_height(info_list):
    conn = None
    command = "UPDATE game_info SET height=%s WHERE codewarsid=%s;"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)
        conn.commit()
        cur.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_time(info_list):
    conn = None
    command = "UPDATE game_info SET time=%s WHERE codewarsid=%s;"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)
        conn.commit()
        cur.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_StartTime(info_list):
    conn = None
    command = "UPDATE game_info SET start_time=%s WHERE codewarsid=%s;"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)
        conn.commit()
        cur.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_height(info_list):
    command = "SELECT height FROM game_info WHERE codewarsid = %s; "
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)

        height = cur.fetchone()[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return height

def get_time(info_list):
    command = "SELECT time FROM game_info WHERE codewarsid = %s; "
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)

        time = cur.fetchone()[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return time

def get_startTime(info_list):
    command = "SELECT start_time FROM game_info WHERE codewarsid = %s; "
    conn = None
    time = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,info_list)

        time = cur.fetchone()[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return time
