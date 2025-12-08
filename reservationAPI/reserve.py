from flask import Flask, request, redirect
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pymysql

app = Flask(__name__)

@app.route("/reserve", methods=["POST"])
def reserve():
    # --- フォームからデータ受け取り ---
    name = request.form["name"]
    email = request.form["email"]
    date = request.form["date"]
    country = request.form.get("country", "")

    # --- MySQL 保存 ---
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="PASS",
        database="reservation_db",
        charset="utf8"
    )
    cur = db.cursor()
    sql = "INSERT INTO reservations (name, email, date, country) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (name, email, date, country))
    db.commit()
    db.close()

    # --- メール送信 ---
    send_reservation_mail(name, email, date, country)

    return redirect("/success")

def send_reservation_mail(name, email, date, country):

    subject = "【予約完了】ご予約ありがとうございます"
    body = f"""
{name} 様

以下の内容で予約を受け付けました。

-------------------------
予約日: {date}
お名前: {name}
メール: {email}
国籍: {country}
-------------------------

当日お会いできることを楽しみにしています。
"""

    # --- メール設定 ---
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = "no-reply@yourdomain.com"
    msg["To"] = email

    # Gmail使用例（推奨：アプリパスワード必要）
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login("yourgmail@gmail.com", "アプリパスワード")
    smtp.sendmail("yourgmail@gmail.com", email, msg.as_string())
    smtp.quit()

@app.route("/success")
def success():
    return """
        <h2>予約が完了しました</h2>
        <p>確認メールを送信しました。</p>
    """

if __name__ == "__main__":
    app.run(debug=True)


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import mysql.connector
# from dotenv import load_dotenv
# import os
# from datetime import datetime
# import uvicorn

# load_dotenv()

# app = FastAPI()

# # CORS設定
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # ==========================
# # MySQL 接続関数
# # ==========================
# def get_connection():
#     return mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         database=os.getenv("MYSQL_DATABASE"),
#         port=os.getenv("MYSQL_PORT")
#     )

# # ==========================
# # フロントから来るデータの型
# # ==========================
# class ReservationData(BaseModel):
#     name: str
#     age: int
#     email: str
#     phone: str
#     nationality: str
#     gender: str
#     date: str   # YYYY-MM-DD

# # ==========================
# # 予約 API
# # ==========================
# @app.post("/reserve")
# def reserve(data: ReservationData):

#     conn = get_connection()
#     cursor = conn.cursor()

#     sql = """
#         INSERT INTO reservations (name, age, email, phone, nationality, gender, date, created_at)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     values = (
#         data.name,
#         data.age,
#         data.email,
#         data.phone,
#         data.nationality,
#         data.gender,
#         data.date,
#         datetime.now()
#     )

#     cursor.execute(sql, values)
#     conn.commit()

#     return {"message": "予約が完了しました！"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5003)
