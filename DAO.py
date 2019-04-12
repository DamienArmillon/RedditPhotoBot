import sqlite3
import time

class Dao:
    def __init__(self):
        """Create the table we will work on"""
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS cooldown (chatId int PRIMARY KEY, cooldown int, lastCall int NOT NULL)")
        conn.commit()
        conn.close()

    def pushLastCall(self,chatId):
        """Push the last call in the bdd"""
        lastCall = int(time.time())
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("INSERT OR IGNORE INTO cooldown(chatId,lastCall) VALUES (?,?)",[chatId,lastCall])
        curs.execute("UPDATE cooldown SET lastcall=? WHERE chatId=?",[lastCall,chatId])
        conn.commit()
        conn.close()


    def setCooldown(self,chatId,cooldown):
        """Eneable to set a new cooldown"""
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("INSERT OR IGNORE INTO cooldown(chatId,cooldown,lastCall) VALUES (?,?,?)",[chatId,cooldown,0])
        curs.execute("UPDATE cooldown SET cooldown=? WHERE chatId=?",[cooldown,chatId])
        conn.commit()
        conn.close()


    def getTimeInfo(self, chatId):
        """Get the lastCall of a given chatId"""
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("SELECT cooldown, lastCall FROM cooldown WHERE chatId = ?", [str(chatId)])
        return curs.fetchone()

