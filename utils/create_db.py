import sqlite3


def create_prefix_db():
    conn = sqlite3.connect("data/prefix.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute("""CREATE TABLE prefix_data (
                guild_id integer,
                prefix string
            )""") 
        except:
            print('Prefix database already exists, aborted creation job') 