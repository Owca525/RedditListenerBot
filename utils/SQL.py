from main import __location_database__, __name_database__
import sqlite3

async def create_connection():
    return sqlite3.connect(__location_database__ + __name_database__)

async def create_tables(conn,server_id):
    with conn:
        conn.execute(f'''CREATE TABLE IF NOT EXISTS s{server_id} (
                        channel_id INTEGER PRIMARY KEY,
                        server_id INTEGER,
                        user_id INTEGER,
                        creation_timestamp TEXT,
                        url_subreddit TEXT,
                        last_check TEXT,
                        last_check_timestamp TEXT,
                        FOREIGN KEY (server_id) REFERENCES servers (id))''')

async def add_data(conn, server_id, data):
    """channel_id, server_id_id, user_id, creation_timestamp, url_subreddit, last_check, last_check_timestamp"""
    sql = f'''INSERT INTO s{server_id} (channel_id, server_id, user_id, creation_timestamp, url_subreddit, last_check, last_check_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    with conn:
        conn.execute(sql, data)

async def get_data(conn, server_id):
    sql = f'''SELECT channel_id, user_id, creation_timestamp, url_subreddit, last_check, last_check_timestamp
             FROM s{server_id}'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

async def get_all_data(table):
    conn = sqlite3.connect('./db/reddit.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM s{table}")
    return cursor.fetchall()

async def delete_data(conn, server, id):
    sql = f'''DELETE FROM s{server} WHERE channel_id = ?'''
    with conn:
        conn.execute(sql, (id,))

async def update_data(table, id, new, old):
    conn = sqlite3.connect('./db/reddit.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE s{table} SET {id} = ? WHERE {id} = ?", (new, old))
    conn.commit()
    
    conn.close()
