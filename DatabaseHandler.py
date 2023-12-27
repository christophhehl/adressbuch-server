import json
import sqlite3


def get_adresses(cursor):
    cursor.execute("SELECT * FROM adressen")
    unformatted = cursor.fetchall()
    formatted = {}
    for adress in unformatted:
        formatted[adress[0]] = adress[1:]
    return json.dumps(formatted)


def get_searched_adresses(cursor, path):
    path = path[1:]
    search_texts = path.split("%20")
    formatted = {}
    for search in search_texts:
        search_value = "%" + search + "%"
        cursor.execute(
            "SELECT * FROM adressen "
            "WHERE Nachname like ? OR Vorname LIKE ? OR Ehepartner LIKE ? OR Straße LIKE ? OR Hausnummer LIKE ? OR "
            "Postleitzahl LIKE ? OR Ort LIKE ? OR Kinder LIKE ?", [search_value] * 8)
        unformatted = cursor.fetchall()
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
                        Ort          varchar(255),
                        Kinder       varchar(255)
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
    return connection


def add_contact(connection, data):
    cursor = connection.cursor()
    print(data)
    if data[0] == '-1':
        cursor.execute(
            "INSERT INTO adressen (nachname, vorname, ehepartner, straße, hausnummer, postleitzahl, ort, kinder)"
            " values (?,?,?,?,?,?,?,?)",
            data[1:])
    else:
        reordered_data = data[1:]
        reordered_data.append(data[0])
        print(reordered_data)
        cursor.execute(
            "UPDATE adressen SET Nachname=?,Vorname=?,Ehepartner=?,Straße=?,Hausnummer=?,Postleitzahl=?,Ort=?,Kinder=? "
            "WHERE id = ?", reordered_data)
    connection.commit()


def delete_contact(connection, id_string):
    cursor = connection.cursor()
    entry_id = int(id_string)
    cursor.execute("DELETE FROM adressen WHERE id = ?", [entry_id])
    connection.commit()
