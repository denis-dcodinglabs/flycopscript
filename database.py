import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = "dbname=flycop user=flycop host=104.199.31.112 password=flycop port=5432" 
def save_flights(flights, from_location, to_location, day, url):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id SERIAL PRIMARY KEY,
            date TEXT,
            time TEXT,
            flight_number TEXT,
            price TEXT,
            from_location TEXT,
            to_location TEXT,
            created_at TIMESTAMP,
            website TEXT
        )
    ''')

    for flight in flights:
        price = flight['price'] if flight['price'] is not None else 'N/A'
        cursor.execute('''
            INSERT INTO flights (date, time, flight_number, price, from_location, to_location, created_at, website)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            flight['date'],
            flight['time'],
            flight['flight_number'],
            price,
            from_location,
            to_location,
            datetime.now(),
            url
        ))
        print(f"Inserted flight: {flight}")

    conn.commit()
    conn.close()