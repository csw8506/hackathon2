from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime
import uvicorn

load_dotenv()

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================
# MySQL 接続関数
# ==========================
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=os.getenv("MYSQL_PORT")
    )

# ==========================
# フロントから来るデータの型
# ==========================
class ReservationData(BaseModel):
    name: str
    age: int
    email: str
    phone: str
    nationality: str
    gender: str
    date: str   # YYYY-MM-DD

# ==========================
# 予約 API
# ==========================
@app.post("/reserve")
def reserve(data: ReservationData):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO reservations (name, age, email, phone, nationality, gender, date, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data.name,
        data.age,
        data.email,
        data.phone,
        data.nationality,
        data.gender,
        data.date,
        datetime.now()
    )

    cursor.execute(sql, values)
    conn.commit()

    return {"message": "予約が完了しました！"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5003)
