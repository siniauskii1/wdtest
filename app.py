from flask import Flask, request
from config import *
import time
import psycopg2
conn = psycopg2.connect(dbname=db, user=user,
                        password=password, host=host)
cursor = conn.cursor()
app=Flask(__name__)

@app.route('/HealthChecker',methods = ['POST'])
def testreq():
    if request.method=='POST':
        try:
            jsonStr = request.get_json()
            token = jsonStr['token']
            problem = jsonStr['problem']
            cursor.execute(f"UPDATE Project SET isworking=1,lastupdate='{time.time()}'  WHERE token='{token}'")
            conn.commit()
        except Exception as err:
            print(err)
    return "Ok"

def server():
    app.run(port=8080)



if __name__ == '__main__':
    server()

