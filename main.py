import sqlite3

import database

print("erste Zeile")

x=7

print("Zweite Zeile")

y=8

print("deine mutter")

z=9
database.meineFunktion()
print("Boje ist ein kleiner Fiker")

verbindung = sqlite3.connect("C:\SQLiteStudio/"
                             "production")
zeiger = verbindung.cursor()
sql_anweisung = """
    CREATE TABLE produktion (
    Date DATE,
    Time TIME,
    Cons_Prod VARCHAR(20),
    Location  VARCHAR(50),
    Energynetwork VARCHAR(50),
    Power DOUBLE(8,2),
    Energysource VARCHAR(50)
    );"""

zeiger.execute(sql_anweisung)

verbindung.commit()
verbindung.close()

b=9

print("Boje ist ein kleiner Fiker")
