import sqlite3

class Dao:
    def __init__(self):
        """Create the table we will work on"""
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS cooldown (chatId int PRIMARY KEY, cooldown int, lastCall int)")
        conn.commit()
        conn.close()

    def getLastCall(self, chatId):
        """Get the lastCall of a given chatId"""
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("SELECT * FROM cooldown WHERE chatId = ?", chatId)
        result = curs.fetchone()
        if result :     #If result is not empty : the chatId is known , return None otherwise
            return result[2]


    def newCooldown(self,chatId,cooldown):
        """Eneable to set a new cooldown"""
        conn = sqlite3.connect("RedditBot.db")
        curs = conn.cursor()
        curs.execute("INSERT OR IGNORE INTO cooldown(chatId,cooldown) VALUES (?,?)",[chatId,cooldown])
        curs.execute("UPDATE cooldown SET cooldown=? WHERE chatId=?",[cooldown,chatId])
        conn.commit()
        conn.close()