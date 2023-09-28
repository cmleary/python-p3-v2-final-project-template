import sqlite3

CONN = sqlite3.connect('players.db')
CURSOR = CONN.cursor()