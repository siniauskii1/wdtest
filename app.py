from flask import Flask, request
import time, psycopg2, telebot
from configs.telegram_config import *
from configs.bd_config import *
bot = telebot.TeleBot(token)

conn = psycopg2.connect(dbname=db, user=user,
                        password=password, host=host)

cursor = conn.cursor()
app=Flask(__name__)

@app.route('/HealthChecker',methods = ['POST','GET'])
def testreq():
    if request.method == 'GET':
        try:
            jsonStr = "fdsf"
            #request.get_json()
            global problem
            global name
            #print(jsonStr)
            #problem = jsonStr['problem']
            #problem = problem.replace('"', '')
            #problem = problem.replace("'", "")
            bot.send_message('885627954', "Your project " + " is working now!")
            return "pok"
            token = jsonStr['token']

            cursor.execute( f"SELECT isworking FROM Project WHERE token='{token}'" )
            isworking = cursor.fetchone()[0]




            cursor.execute(f"SELECT projectname FROM Project WHERE token='{token}'")
            name = cursor.fetchone()[0]
            print(problem)
            if not isworking and problem=="HCk":

                cursor.execute(f"UPDATE Project SET lastupdate='{time.time()}' WHERE token='{token}'")

                cursor.execute(f"UPDATE Project SET isworking=1 WHERE token='{token}'")
                # ------------------------------ДЛЯ ТЕЛЕГРАМ----------------------------------
                cursor.execute(f"SELECT user_id FROM Users WHERE token='{token}'")
                users = cursor.fetchall()

                for items in users:
                    bot.send_message(items[0], "Your project " + name + " is working now!")
                # ---------------------------------ДЛЯ ДИСКОРДА--------------------------------
                cursor.execute(f"SELECT user_id, chat_id FROM DiscordUsers WHERE token='{token}'")
                users = cursor.fetchall()
                for items in users:
                    print(items)
                    cursor.execute(f"INSERT INTO discordwait(user_id, chat_id , problem) VALUES ({items [ 0 ]},{items[1]},'Your project {name} is working now!')" )

            elif problem != "HCk":
                print("1" + problem)
                cursor.execute(f"UPDATE Project SET lastupdate='{time.time()}' WHERE token='{token}'")

                cursor.execute(f"UPDATE Project SET isworking=0 WHERE token='{token}'")
                # ------------------------------ДЛЯ ТЕЛЕГРАМ----------------------------------
                cursor.execute(f"SELECT user_id FROM Users WHERE token='{token}'")
                users = cursor.fetchall()

                for items in users:
                    bot.send_message(items[0], f"Your project {name} is crashed with error {problem}")
                # ---------------------------------ДЛЯ ДИСКОРДА--------------------------------
                cursor.execute( f"SELECT user_id, chat_id FROM DiscordUsers WHERE token='{token}'" )

                users = cursor.fetchall()
                for items in users:
                    cursor.execute(f"INSERT INTO discordwait(user_id, chat_id ,problem) VALUES ({items[0]},{items[1]},'Your project {name} is crashed with error {problem}')")

            else:
                cursor.execute(f"UPDATE Project SET lastupdate='{time.time()}' WHERE token='{token}'")
            conn.commit()

        except Exception as err:
            print("Программа закончила работу с ошибкой: \n"+str(err))
    return "Ok"

@app.route('/CucleChecker',methods = ['POST'])
def testreq2():
    if request.method == 'POST':
        try:
            jsonStr = request.get_json()
            mes = jsonStr
            token = jsonStr['token']
            text = f"[Warning] {jsonStr['message']}"
            print(text)
            # Добавить в базу данных, вместе с логами. Если логов больше ста удалить их нахуй и вставить наш последним
            # Отправить сообщение челу в тг ну и для дс
        except:
            pass
    return "Ok"

@app.route('/MakeLog',methods = ['POST'])
def testreq3():
    if request.method == 'POST':
        try:
            jsonStr = request.get_json()
            tag = jsonStr["tag"] #тег лога, его указывает пользователь.
            token = jsonStr["token"] #токен
            info = jsonStr["info"] #сам лог
            text = f"[{tag}] {info}" #это в базу данных засунуть и отправить в телегу
            print(text)
            #Добавить в базу данных лог, Если логов больше ста удалить их нахуй и вставить наш последним
            #Отправить сообщение челу в тг ну и для дс

        except:
            pass
    return "Ok"




def server():
   app.run(port=8080)

if __name__ == '__main__':
    server()

