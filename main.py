import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
import time
import requests
import random
import os

from conf import token, botName, userAgent, spamTime, subreddit

with open("info.txt",'w') as info :
    #Create a info.txt file with the process to kill to rebot the bot and a text to copy to botfather to set command
    info.write("process id : " + str(os.getpid())+"\n")
    inlineHelp = ["{} - send photo from r/{} to the group\n".format(tag,subreddit[tag]) for tag in subreddit]
    info.writelines(inlineHelp)



class PhotoSender(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(PhotoSender, self).__init__(*args, **kwargs)
        self.lastCall = -50.0
        self.isAbuse = False

    def dealAbuse(self, chatId, msgId):
        """Si le bot a été appelé trop récement il n'enverra pas de photos"""
        if time.time() - self.lastCall < spamTime:  # Le bot ne permet d'envoyer des images que toutes les 30s/chan
            if self.isAbuse:
                bot.deleteMessage((chatId, msgId))
            else:
                bot.sendMessage(chatId, 'Je ne peux pas spammer des photos', reply_to_message_id=msgId)
                self.isAbuse = True
        else:
            self.isAbuse = False
        return self.isAbuse

    def isImage(self, url):
        """Renvoie true si l'url est l'url d'une image et false sinon"""
        recognisedFormat = ['.jpg', '.png', '.jpeg']
        for oneFormat in recognisedFormat:
            if url.endswith(oneFormat):
                return True
        return False

    def sendReddit(self,tag ,chatId, msgId):
        """Va chercher plein d'url de photo sur reddit et en sélectionne 1 qu'il renvoie"""
        res = requests.get('https://www.reddit.com/r/'+tag+'/hot/.json',
                           headers={'User-Agent': userAgent},
                           params={'limit': 100})
        imgIndex = random.randint(0, 100)
        url = res.json()["data"]["children"][imgIndex]['data']["url"]
        while not (self.isImage(url)):
            imgIndex = random.randint(0, 100)
            url = res.json()["data"]["children"][imgIndex]['data']["url"]
        bot.sendPhoto(chatId, url, reply_to_message_id=msgId)

    def checkAndSend(self,msg):
        """Check if the tag is used as a command in the message and send the corresponding photo if it's the case.
        If it send a photo, it returns true"""
        contentType, chatType, chatId = telepot.glance(msg)
        text = msg['text'].split(' ')
        msgId = msg['message_id']
        for tag in subreddit :
            if '/{}'.format(tag) in text or '/{}@{}'.format(tag,botName) in text:
                if chatType=='private' or not (self.dealAbuse(chatId, msgId)):
                    self.lastCall = time.time()
                    self.sendReddit(subreddit[tag],chatId, msgId)
                    return True
        return False


    def on_chat_message(self, msg):
        contentType, chatType, chatId = telepot.glance(msg)
        if contentType == 'text':
            text = msg['text'].split(' ')
            # For All reddit chan, its all in one function
            if self.checkAndSend(msg) :
                return None
            if '/help' in text or '/help@'+botName in text:
                bot.sendMessage(chatId, "Hi I'm a super bot sending to you icredible reddit content")
                return None


bot = telepot.DelegatorBot(token, [pave_event_space()(per_chat_id(), create_open, PhotoSender, timeout=45), ])
MessageLoop(bot).run_as_thread()
while True:
    time.sleep(1)
