from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#dictionary of words to replace
replace = { "America": "the Earth",
			"Americans": "nature",
			"anti-gun": "anti-Green",
			"anti-guns": "anti-Green",
			"Assault": "Climate",
			"assault": "climate",
			"assault-weapon": "climate change",
			"ban": "emissions",
			"bill": "emissions",
			"control": "change",
			"#DefendtheSecond": "#DefendtheEarth",
			"gun": "climate",
			"guns": "climate",
			"gun-control": "global warming",
			"#guncontrol": "#climatechange",
			"jihadist": "global warming",
			"jihadists": "global warming",
			"laws": "change",
			"rifle": "change",
			"right": "planet",
			"rights": "planet",
			"Terror": "Global Warming",
			"terror": "global warming",
			"Terrorism": "Global Warming",
			"terrorism": "global warming",
			"terrorist": "climate change",
			"terrorists": "climate change",
			"#2A": "#Earth"

			}


def getNRATweet():
	"""
	Gets the NRA's most current tweet
	"""
	nra_timeline = twitter.get_user_timeline(screen_name="NRA",count=1)
	for tweet in nra_timeline:
		#print(tweet['text'].encode('utf8')).decode('utf8')
		print("Got NRA Tweet!")
		return tweet['text'].encode('utf8').decode('utf8')





def makeNewTweet(nraTweetWords):
	"""
	Takes a list of words nraTweetWords
	and makes it about climate
	"""
	numEdits = 0				#counter of number of changes made to tweet
	newWords = []				#put new tweet in this list
	index = 0					#index of current word being looked at

	for x in nraTweetWords:		#for each word in the tweet
		havePunc = False		#whether or not it has punctuation
		punc = ''

		#the current character count of the tweet
		currLen = len(' '.join(newWords[:index] + nraTweetWords[index:]))

		#if there is punctuation with the word being checked
		if x[-1] == ',' or x[-1] == '.' or x[-1] == '?' or x[-1] == '!' or x[-1] == ':' or x[-1] == ';':
			havePunc = True		#it has punctuation
			punc = x[-1:]		#store the punctuation for later
			X = x[:-1]			#save just the word
		else:					#Otherwise, just keep the word
			X = x

		if X == '&amp':
			newWords.append('&')
		elif X in replace and len(replace[X] + punc) - len(X + punc) + currLen <= 140:	#if it's a key word and adding it  doesn't put tweet over 140 char
			newWords.append(replace[X] + punc)											#replace it
			numEdits += 1						    									#add to the number of edits
		elif X.lower() in replace and len(replace[X.lower()] + punc) - len(X.lower() + punc) + currLen <= 140:
			newWord = replace[X.lower()]												#check for capitalization					
			newWords.append(newWord[0].capitalize() + punc)
			numEdits += 1
		else:									   										#else don't change it
			newWords.append(X + punc)
		index += 1


	currLen = len(' '.join(newWords))		#update current character count
	print("Character Count:",currLen)
	if(numEdits < 1):						#if no changes
		return None							#return none
	return newWords 						#otherwise return the new tweet


	

def tweet(tweet):
	"""
	Tweet a string
	"""
	twitter.update_status(status = tweet);



lastTweet = None		#to store the last tweet that was edited by the bot

def runBot():
	print("Bot running!")

	nraTweet = getNRATweet()						#Get the NRA's latest tweet
	#nraTweet = ""

	global lastTweet

	if nraTweet != lastTweet:						#make sure the bot hasn't edited the tweet before
		nraTweetWords = nraTweet.split()			#turn the tweet into a list of words
		try:
			print(nraTweet)
		except:
			print("Cannot print")


		newTweetWords = makeNewTweet(nraTweetWords)	#Edit the tweet

		if newTweetWords == None:					#if no changes
			print("No changes to tweet!")
		else:
			newTweet = ' '.join(newTweetWords) 		#Join tweet into string
			try:
				print(newTweet)
			except:
				print("Cannot print new tweet")

			if (not debug):							#if not in debug mode
				try:
					tweet(newTweet)					#tweet new tweet
					print("I just tweeted!")
				except:
					print("Ran into a problem tweeting!")

		lastTweet = nraTweet 						#Set this to latest tweet
	else:
		print("No new Tweet!")


def setInterval(func, sec):
	def func_wrapper():
		setInterval(func, sec)
		func()
	t = Timer(sec, func_wrapper)
	t.start()
	return t


debug = False
runOnce = True

runBot()
if not runOnce:
	setInterval(runBot, 60*60*1)		#runs every hour