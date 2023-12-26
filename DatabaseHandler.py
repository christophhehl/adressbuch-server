import json
import sqlite3


def get_adresses(cursor):
    cursor.execute("SELECT * FROM adressen")
    unformatted = cursor.fetchall()
    formatted = {}
    for adress in unformatted:
        formatted[adress[0]] = adress[1:]
    return json.dumps(formatted)


def create_adressen_table(cursor):
    cursor.execute("""
                    CREATE TABLE adressen
                    (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        Nachname     varchar(255),
                        Vorname      varchar(255),
                        Ehepartner   varchar(255),
                        Straße       varchar(255),
                        Hausnummer   varchar(255),
                        Postleitzahl varchar(255),
                        Ort          varchar(255)
                    )
    """)


def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adressen'")
    result = cursor.fetchall()
    print(result)
    if not result:
        create_adressen_table(cursor)


def connect_or_create():
    connection = sqlite3.connect("adressbuch.db")
    create_tables(connection)
    return connection.cursor()
