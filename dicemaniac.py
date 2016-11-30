from slackbot.bot import respond_to
from slackbot.bot import listen_to
from os.path import dirname
from slackbot.bot import Bot
import inspect
import sys
import re
import random

sys.path.append(dirname("/home/jbird/dicemaniac/"))
# to get the slackbot_settings.py file that contains the API token

# some default info
DEFAULT_REPLY = "Sorry but I'm a complete tosser"
ERRORS_TO = 'jeremy'
MAX_DICE = 200  # just to prevent insane scenarios
MAX_SIDES = 9002 #
#
# some joke values, hidden from public view
ANTI_ROSS = False
#PLUGINS = [
#    'slackbot.plugins',
#    'mybot.plugins',
#]
#

######
# IMPORTANT MACROS
###
def tx(message):
    return message._body.get('text')
###
def n1(message):
    return re.findall('[\d]+',re.findall('[\d]+[dD]',message).pop(0)).pop(0)
###
def n2(message):
    return re.findall('[\d]+',re.findall('[dD][\d]+',message).pop(0)).pop(0)
###
def n3(message):
    return re.findall('[\d]+',re.findall('[\+-][\d]+$',message).pop(0)).pop(0)
def getDice(message):
    return int(n1(message))
###
def getSides(message):
    return int(n2(message))
###
def getMod(message):
    return int(n3(message))
###
#####

### custom plugins. let's see if this actually works.
@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')

@listen_to('love', re.IGNORECASE)
def love(message):
    message.react('heart')

@listen_to('sweet, summer child', re.IGNORECASE)
def summerchild(message):
    message.reply('http://i.imgur.com/qsSj2L6.gif')

### We want to be able to do a /\d+[dD]\d+/ scenario as well as one without preceding digits.
##@listen_to('[dD][\d]+$')
##def roll(message):
##    resString = None
##    if (re.search('[\d]+[dD][\d]+$',tx(message))):
##        if(re.search('-[\d]+[dD][\d]+$',tx(message))):
##            message.reply("I can't roll a negative number of dice!")
##        elif(getDice(tx(message) == 0):
##            message.reply("You're hilarious.")
##        elif(getDice(tx(message) == 1):
##            message.reply("Why even bother specifying one die? Are you crazy?")
##        elif(getDice(tx(message) > MAX_DICE):
##            message.reply("That's a few more than I'm willing to roll. My hand's aren't nearly big enough!")
##        elif(getSides(tx(message) == 0):
##            message.reply("Not really happy about this.")
##        elif(getSides(tx(message) == 1):
##            message.reply("yeah yeah whatever")
##        elif(getSides(tx(message)) > MAX_SIDES):
##            message.reply("That's basically a ball at this point.")
##        else:
##            results = []
##            for i in range(0,getDice(tx(message)):
##                results.append(random.randrange(1,getSides(tx(message)))
##            resString = ', '.join(map(str,results))
##    else:
##        if(getSides(tx(message) == 0):
##            message.reply("I LITERALLY CAN'T.")
##        elif(getSides(tx(message) == 1):
##            message.reply("I _could_, but I won't.")
##        elif(getSides(tx(message) > MAX_SIDES):
##            message.reply("That's basically a ball at this point.")
##        else:
##            resString = str(random.randrange(1,getSides(tx(message)))
##    if(resString):
##        message.reply("Your results: " + resString)

# Revamped roll function. Checking for + and - modifiers at the end. Maybe separate functions per scenario?
@listen_to('(\d+)?[dD](\d+[\+-])?\d+$')
def roll(message):
    resString = None
    total = 0
    catch = re.findall('(\d+)?[dD](\d+[\+-])?\d+$',tx(message)).pop(0)

    if (re.search('\d+[dD]',catch)):
        if (getDice(catch) == 0):
            message.reply("You're hilarious.")
        elif (getDice(catch) == 1):
            message.reply("Why even bother rolling one die? Are you crazy?")
        elif (getDice(catch) > MAX_DICE):
            message.reply("That's a few more than I'm willing to roll. My hands aren't nearly big enough!")
        elif (getSides(catch) == 0):
            message.reply("Why do you hate me?")
        elif (getSides(catch) == 1):
            message.reply("1. The answer is 1. I don't care what you were expecting.")
        elif (getSides(catch) > MAX_SIDES):
            message.reply("That's basically a ball at this point.")
        elif (re.search('[\+-]',catch) and getMod(catch) == 0):
            message.reply("This joke is really overplayed.")
        elif (re.search('[\+-]',catch) and getMod(catch) > MAX_MOD):
            message.reply("Can't have that big of a mod, I'm afraid. Try something lower.")
        else:
            results = []
            for i in range(0,getDice(catch)):
                roll = random.randrange(1,getSides(catch))
                results.append(roll)
                total += roll
            resString = ', '.join(map(str,results))
            if (re.search('\+',catch)):
                total += getMod(catch)
            elif (re.search('-',catch)):
                total -= getMod(catch)
            resString = 'Total: ' + str(total) + '. Rolls: ' + resString



#    message.reply('You said: ' + message._body.get('text'))
#    print(tx(message))
#    message.reply('You want me to roll a ' + re.findall('[\d]+',re.findall('[dD][\d]+$',tx(message)).pop(0)).pop(0))
###

# main loop
def main():
    bot = Bot()
    bot.run()

# no idea why this is necesary but the docs said to put this here lol
if __name__ == "__main__":
    main()
