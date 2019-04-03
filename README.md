# RedditPhotoBot
A customisable Telegram Bot to send photo from reddit

If you want to have a bot sending random photo on Telegram : nothing is easier !

You just have to clone the repo and fil the [temp_conf.py](temp_conf.py) as temp.py with the informations:

* The token of the bot
* The userName of your bot (without the @)
* The cooldown in second between two photo (an antispam security for chan. If you don't want it put it to)
* A dictionary with the different commands you want associated to the list of the subreddits you want to pick photo
* A user agent for Reddit (necessary !)

Then just run main and enjoy !
