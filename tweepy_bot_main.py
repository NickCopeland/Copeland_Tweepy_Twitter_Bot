import sys
sys.path.insert(0,'C:/Users/Nick/source/repos')
import tweepy
import logging
from github_twitter_config import create_api
import json
import time
import datetime
from twitter_keywords import return_bad_keywords


def start_log():
    """Start of log file"""
    logging.info("----------------Start of Log----------------")

def end_log():
    """End of log file"""
    logging.info("----------------End of Log------------------")

def logp(s):
    """Print and write a string to the log"""
    print(s)
    logging.info(s)

def log_error_string():
    """Write error to log file along with error details"""
    logging.info('ERROR: \nError Description: {} \nError at line: {}'.format(sys.exc_info()[1], sys.exc_info()[2].tb_lineno))

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        print("Initialized API")


    def on_status(self, tweet):
        """
        Process newly streamed tweets.

        When a new tweet is streamed it will go through validations and then get retweeted or favorited.
        """

        if tweet.in_reply_to_status_id is not None:
            print(f"Processing tweet {tweet.id} - Bad tweet: tweet is a reply")
            return
        if tweet.user.id == self.me.id:
            print(f"Processing tweet {tweet.id} - Bad tweet: user = me")
            return
        
        if not tweet.retweeted:
            try:
                #---------------------------------------------------------------------------------------------------------------------#
                # Check - must include picture
                #---------------------------------------------------------------------------------------------------------------------#
                pictureFound = False
                killTweet = False
                for media in tweet.entities.get("media",[{}]):
                    if media.get("type",None) == "photo":
                        pictureFound = True
                if pictureFound == False:
                    print(f"Processing tweet {tweet.id} - Bad tweet: no picture")
                    killTweet = True
                    return
                

                #---------------------------------------------------------------------------------------------------------------------#
                # Check - no URLs in tweet allowed
                #---------------------------------------------------------------------------------------------------------------------#
                for media in tweet.entities.get("urls",[{}]):
                    if media.get("display_url",None) is not None:
                        print(f"Processing tweet {tweet.id} - Bad tweet: url found")
                        killTweet = True
                        return
                


                #---------------------------------------------------------------------------------------------------------------------#
                # Check - tweet must include text
                #---------------------------------------------------------------------------------------------------------------------#
                if hasattr(tweet, 'text'):
                    if tweet.text is None:
                        print(f"Processing tweet {tweet.id} - Bad tweet: text field not included")
                        killTweet = True
                        return
                else:
                    print(f"Processing tweet {tweet.id} - Bad tweet: no tweet attribute")
                    killTweet = True
                    return
                
                #---------------------------------------------------------------------------------------------------------------------#
                # Check - tweet is regular tweet or a retweet
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    if tweet.text.lower().startswith("rt @"):
                        killTweet = True
                        print(f"Processing tweet {tweet.id} - Bad tweet: tweet was a retweet")
                        return


                #---------------------------------------------------------------------------------------------------------------------#
                # Check - possibly_sensitive
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    # check if possibly_sensitive attribute = true
                    if hasattr(tweet, 'possibly_sensitive'):
                        if tweet.possibly_sensitive == True:
                            print(f"Processing tweet {tweet.id} - Bad tweet: sensitive content")
                            killTweet = True
                            return
                    else:
                        print (f"Processing tweet {tweet.id} - Bad tweet: Tweet doesn't have possibly_sensitive attribute")
                        killTweet = True
                        return


                #---------------------------------------------------------------------------------------------------------------------#
                # Check - how old the tweet is
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    currentUTCTime = datetime.datetime.utcnow()
                    tweetAge = currentUTCTime.timestamp() - (tweet.created_at - datetime.datetime(1970,1,1)).total_seconds() - 25200
                    
                    # Don't retweet anything older than a week (604k seconds)
                    if tweetAge > 604800:
                        killTweet = True
                        print(f"Processing tweet {tweet.id} - Bad tweet: too old - " + str(tweet.created_at))
                        return


                #---------------------------------------------------------------------------------------------------------------------#
                # Check - user attributes (bio + username)
                #---------------------------------------------------------------------------------------------------------------------#
                if hasattr(tweet, 'user'):
                    if hasattr(tweet.user, 'description'):
                        # tweet author bio
                        if tweet.user.description is None:
                            print(f"Processing tweet {tweet.id} - Bad tweet: bio not included")
                            killTweet = True
                            return
                    else:
                        print(f"Processing tweet {tweet.id} - Bad tweet: user.description attribute not included")
                        killTweet = True
                        return
                    if hasattr(tweet.user, 'screen_name'):
                        #  tweet author username
                        if tweet.user.screen_name is None:
                            print(f"Processing tweet {tweet.id} - Bad tweet: username not included")
                            killTweet = True
                            return
                    else:
                        print(f"Processing tweet {tweet.id} - Bad tweet: user.screen_name attribute not included")
                        killTweet = True
                        return
                else:
                    print(f"Processing tweet {tweet.id} - Bad tweet: no user attribute")
                    killTweet = True
                    return

                #---------------------------------------------------------------------------------------------------------------------#
                # Check - bad keyword check #1: tweet text
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    # Check if forbidden keywords used
                    forbiddenKeywordFound = [ele for ele in badKeywordsTweetText if(ele in tweet.text.lower())]
                    if bool(forbiddenKeywordFound) == True:
                        print(f"Processing tweet {tweet.id} - Bad tweet: unwanted keyword found - " + str(forbiddenKeywordFound))
                        print("     full text: " + str(tweet.text.replace('\n', ' ').replace('\r', '').encode('ascii',errors='ignore')))
                        killTweet = True
                        return
                
                #---------------------------------------------------------------------------------------------------------------------#
                # Check - bad keyword check #2: bio
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    # Check if forbidden keywords used
                    forbiddenKeywordFound = [ele for ele in badKeywordsUserBio if(ele in tweet.user.description.lower())]
                    if bool(forbiddenKeywordFound) == True:
                        print(f"Processing tweet {tweet.id} - Bad tweet: unwanted bio keyword found - " + str(forbiddenKeywordFound))
                        print("     full bio: " + str(tweet.user.description.replace('\n', ' ').replace('\r', '').encode('ascii',errors='ignore')))
                        killTweet = True
                        return

                #---------------------------------------------------------------------------------------------------------------------#
                # Check - bad keyword check #3: username
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    # Check if forbidden keywords used
                    forbiddenKeywordFound = [ele for ele in badKeywordsUsername if(ele in tweet.user.screen_name.lower())]
                    if bool(forbiddenKeywordFound) == True:
                        print(f"Processing tweet {tweet.id} - Bad tweet: unwanted username keyword found - " + str(forbiddenKeywordFound))
                        print("     full username: " + str(tweet.user.screen_name.replace('\n', ' ').replace('\r', '').encode('ascii',errors='ignore')))
                        killTweet = True
                        return
                
                    
                #---------------------------------------------------------------------------------------------------------------------#
                # Check - bad keyword check #4: user profile website
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    if hasattr(tweet.user, 'url'):
                        if tweet.user.url is not None:
                            forbiddenKeywordFound = [ele for ele in badKeywordsUsername if(ele in tweet.user.url.lower())]#badKeywordsUsername
                            if bool(forbiddenKeywordFound) == True:
                                print(f"Processing tweet {tweet.id} - Bad tweet: unwanted user profile website - " + str(forbiddenKeywordFound))
                                killTweet = True
                                return


                #---------------------------------------------------------------------------------------------------------------------#
                # Check - is tweet a quote tweet
                #---------------------------------------------------------------------------------------------------------------------#
                if killTweet == False:
                    if hasattr(tweet, 'quoted_status'):
                        print("quoted_status found")
                        if tweet.quoted_status is not None:
                            print("quoted_status is not none")
                            print(f"Processing tweet {tweet.id} - Bad tweet: tweet is quote tweet")
                            killTweet = True
                            return


                #---------------------------------------------------------------------------------------------------------------------#
                # Retweet
                #---------------------------------------------------------------------------------------------------------------------#
                if retweetTweet == True and pictureFound == True and killTweet == False:
                    tweet.retweet()
                    print(f"Processing tweet {tweet.id} - retweeted---------------------------------------------------------------------")
                

                #---------------------------------------------------------------------------------------------------------------------#
                # Favorite
                #---------------------------------------------------------------------------------------------------------------------#
                if favoriteTweet == True and pictureFound == True and killTweet == False:
                    tweet.favorite()
                    print(f"Processing tweet {tweet.id} - favorited---------------------------------------------------------------------")
            except Exception as e:
                logp("Error on fav and retweet: " + str(e))

    def on_error(self, status):
        # Log error
        logp("ERROR: " + status)
        log_error_string()

        # kill program if error = 420 (rate limit issue)
        if status == 420:
            # End the program by returning false to on_status when Twitter returns error 420 as a rate limit
            # to avoid them punishing you for too many data requests.
            logp("Ending program to avoid rate limit consequences")
            return False

def stream_tweets(keywords):
    # Start twitter API
    api = create_api()
    logp("api created")

    tweets_listener = FavRetweetListener(api)
    print("tweets listener created")
    stream = tweepy.Stream(api.auth, tweets_listener)
    print("stream created")
    stream.filter(track=keywords, languages=["en"], filter_level="low")
    print("stream filter created")

if __name__ == "__main__":
    try:
        # Logging
        log_path = __file__.replace(".py", ".txt")
        logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s %(message)s')
        start_log()
    
        # Variables
        retweetTweet = True
        favoriteTweet = True
    
        # Keywords to stream in seperated lists by topic for easy updating
        # Example keywords given for streaming home economics related tweets
        keywordsHealth = ['#nutrition', '#health']
        keywordsCooking = ['#cooking', '#baking', '#food', '#recipe', '#foodie', '#breakfast', '#brunch', '#lunch', '#dinner', '#dessert', '#cookingathome', '#tacos', '#charcuterie']
        keywordsInteriorDesign = ['#interiordesign', '#interiorstyling', '#decor', '#homedecor', '#bedroom', '#livingroom', '#diningroom']
        keywordsHousekeeping = ['#cleaningtips', '#topcleaningtips', '#gardeningtips', '#gardening', '#gardenparty', '#diytips']
    
        # master list
        keywordsSearch = []

        # combine keywords to search
        keywordsSearch.extend(keywordsHealth)
        keywordsSearch.extend(keywordsCooking)
        keywordsSearch.extend(keywordsInteriorDesign)
        keywordsSearch.extend(keywordsHousekeeping)


        # Load bad keyword lists
        badKeywordsTweetText, badKeywordsUserBio, badKeywordsUsername = return_bad_keywords()


        # validate undesirable keyword lists got loaded
        if len(badKeywordsTweetText) == 0:
            logp("ERROR: badKeywordsTweetText list not loaded")
            sys.exit()
        if len(badKeywordsUserBio) == 0:
            logp("ERROR: badKeywordsUserBio list not loaded")
            sys.exit()
        if len(badKeywordsUsername) == 0:
            logp("ERROR: badKeywordsUsername list not loaded")
            sys.exit()

        # Start stream of tweets
        stream_tweets(keywordsSearch)

        # The process will now run until Twitter terminates your connection
    
    # Error handling
    except Exception as e:
        logp(sys.exc_info()[1])

