import psycopg2
from data import departures, tours

conn = psycopg2.connect(
    dbname="flask_travel",  
    user="USER",        
    password="123",  
    host="localhost",       
    port="5432"             
)

cursor = conn.cursor()

for code, name in departures.items():
    cursor.execute(
        "INSERT INTO departures (code, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (code, name)
    )

cursor.execute("SELECT id, code FROM departures")
departures_ids = {code: id for id, code in cursor.fetchall()}

for tour in tours.values():
    cursor.execute(
        """
        INSERT INTO tours (title, description, departure_id, picture, price, stars, country, nights, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            tour['title'],
            tour['description'],
            departures_ids[tour['departure']],  
            tour['picture'],
            tour['price'],
            int(tour['stars']),
            tour['country'],
            tour['nights'],
            tour['date'],
        )
    )

conn.commit()

cursor.close()
conn.close()

print("Дані успішно перенесено до PostgreSQL!")
