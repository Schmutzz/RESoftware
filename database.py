import sqlite3

def meineFunktion(self):
    verbindung = sqlite3.connect("C:\Users\pc102\Desktop\sqlitestudio-3.3.3\SQLiteStudio/production")
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