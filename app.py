from flask import Flask, request
from config import token as ttoken
from config import *
import time
import telebot
import threading
import psycopg2
conn = psycopg2.connect(dbname=db, user=user,
                        password=password, host=host)
cursor = conn.cursor()
app=Flask(__name__)
bot = telebot.TeleBot(ttoken)
Workers = {}

@app.route('/')
def test():
    return "OK"

@app.route('/HealthChecker',methods = ['POST'])
def testreq():

    if request.method=='POST':
        try:
            jsonStr = request.get_json()
            token = jsonStr['token']
            problem = jsonStr['problem']
            Workers[token] = time.time()
            cursor.execute(f"UPDATE Project SET isworking=1  WHERE token='{token}'")
            conn.commit()
        except:
            return  "Bad"

    return "Ok"


def checker():
    while True:
        try:
            copy = Workers.copy().items()
            for a in copy:
                if float(time.time())-float(a[1])>10:
                    #БАЗА ДАННЫХ
                    mytoken = a[0]
                    cursor.execute(f"UPDATE Project SET isworking=0  WHERE token='{mytoken}'")
                    conn.commit()
                    cursor.execute(f"SELECT user_id FROM Users WHERE token='{mytoken}'")
                    allusers = cursor.fetchall()
                    cursor.execute(f"SELECT projectname FROM Project WHERE token='{mytoken}'")
                    projectname = cursor.fetchone()[0]
                    qq = []
                    for i in allusers:
                        qq.append(i[0])
                    print("Users", str(qq))
                    del Workers[a[0]]
                    for b in qq:
                        try:
                            bot.send_message(b,"Ваш сервер, под названием "+projectname+" упал")
                        except:
                            pass
        except:
            pass



def server():
    app.run()



if __name__ == '__main__':
    thr = threading.Thread(target=server)
    thr.start()
    checker()



