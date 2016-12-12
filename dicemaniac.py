from slackbot.bot import respond_to
from slackbot.bot import listen_to
from os.path import dirname
from slackbot.bot import Bot
import inspect
import sys
import re
import random
import pyowm

sys.path.append(dirname("/home/jbird/dicemaniac/"))
# to get the slackbot_settings.py file that contains the API token

# some default info
DEFAULT_REPLY = "Sorry but I'm a complete tosser"
ERRORS_TO = 'jeremy'
MAX_DICE = 200  # just to prevent insane scenarios
MAX_SIDES = 9002 #
MAX_MOD = 200
TOTAL_FRONT = False
#
# some joke values, hidden from public view
ANTI_ROSS = True
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
def getDice(message,default=None):
    if (message[0]):
        return int(message[0])
    else:
        return default
###
def getSides(message,default=None):
    if (message[2]):
        return int(message[2])
    elif (message[4]):
        return int(message[4])
    else:
        return default
###
def getMod(message,default=None):
    if (message[3] and message[4]):
        return int(message[4])
    else:
        return default
###
def getBuff(message,default=None):
    if (message[3]):
        return (message[3])
    else:
        return default
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

@listen_to('relevant xkcd', re.IGNORECASE)
def relevant(message):
    message.reply('I no work yet!')

# Revamped roll function. Checking for + and - modifiers at the end. Maybe separate functions per scenario?
@listen_to('[dD]\d+')
def roll(message):
    if (re.search('(\d+)?[dD](\d+[\+-])?\d+$',tx(message))): 
        resString = None
        total = 0
        catch = re.findall('(\d+)?[dD]((\d+)([\+-]))?(\d+)$',tx(message)).pop(0)
        ONE_TRIG = False
        

        legend = 'Rolls: '
#Created seperate roller function because it was repeated code
        def roller(dice, sides, buff, mod, total, legend):
            results = []
            for i in range(0,dice):
                roll = random.randrange(1,sides+1)
                results.append(roll)
                total += roll
            resString = ', '.join(map(str,results))
            if(total == dice*sides):
                legend = 'Legendary rolls! '
            if (buff == '+'):
                total += mod
            elif (buff == '-'):
                total -= mod
            resString = legend + resString
            return resString,total,legend





        #print("catch: ")
        #print(catch)
        

        if (getDice(catch)):
            if (getDice(catch) == 0):
                message.reply("You're hilarious.")
            elif (getDice(catch) == 1):
                message.reply("Why even bother rolling one die? Are you crazy?")
            elif (getDice(catch) > MAX_DICE):
                message.reply("That's a few more than I'm willing to roll. My hands aren't nearly big enough!")
            elif (getSides(catch) == 0):
                message.reply("Why do you hate me?")
            elif (getSides(catch) == 1):
                ONE_TRIG = True
                resString, total, legend = roller(getDice(catch), getSides(catch), getBuff(catch), getMod(catch), total, legend)
                message.reply("1. The answer is 1. I don't care what you were expecting....But here: " + resString + " Total: " + str(total))
            elif (getSides(catch) > MAX_SIDES):
                message.reply("That's basically a ball at this point.")
            elif (getBuff(catch) and getMod(catch) == 0):
                message.reply("This joke is really overplayed.")
            elif (getBuff(catch) and getMod(catch) > MAX_MOD):
                message.reply("Can't have that big of a mod, I'm afraid. Try something lower.")
            else:
                resString, total, legend = roller(getDice(catch), getSides(catch), getBuff(catch), getMod(catch), total, legend)
        else:
            if (getSides(catch) == 0):
                message.reply("Why do you hate me?")
            elif (getSides(catch) == 1):
                ONE_TRIG = True
                resString, total, legend = roller(getDice(catch), getSides(catch), getBuff(catch), getMod(catch), total, legend)
                message.reply("1. The answer is 1. I don't care what you were expecting....But here: " + resString + " Total: " + str(total))
            elif (getSides(catch) > MAX_SIDES):
                message.reply("That's basically a ball at this point.")
            elif (getBuff(catch) and getMod(catch) == 0):
                message.reply("This joke is really overplayed.")
            elif (getBuff(catch) and getMod(catch) > MAX_MOD):
                message.reply("Can't have that big of a mod, I'm afraid. Try something lower.")
            else:
                if(ANTI_ROSS and getSides(catch)==20 and re.search('[rR][oO][sS][sS]',tx(message))):
                    result = 20
                #elif (getSides(catch)==2 and not getBuff(catch)):
                #    if (random.randrange(1,3) == 1):
                #        result = 'Heads!'
                #    else:
                #        result = 'Tails!'
                else:
                    resString, total, legend = roller(getDice(catch), getSides(catch), getBuff(catch), getMod(catch), total, legend)
        if (resString and ONE_TRIG == False):
            if (getBuff(catch) or getDice(catch)):
                if (TOTAL_FRONT):
                    resString = 'Total: ' + str(total) + '. ' + resString
                else:
                    resString = resString + '. Total: ' + str(total)
            message.reply("Your results:   " + resString)
    #else:
    #    print ("Unmatching message caught.") # this is just for debugging.
##
 

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
