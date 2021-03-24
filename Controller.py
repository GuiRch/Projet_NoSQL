import sqlite3
import json
from utils import jsonToDict

def save_sql(username,encrypt):
    ciphertext = encrypt[0]
    nonce = encrypt[1]
    key = encrypt[2]
    
    data = (username, ciphertext, nonce, key)
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(" INSERT INTO users (username, ciphertext, nonce, key) VALUES ( ?, ?, ?, ?) ",data)
    # the secure way to enter the variable
    conn.commit()
    conn.close()
    
