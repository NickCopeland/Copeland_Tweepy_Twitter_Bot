import tweepy
import logging
import os



def create_api():
    """Set up tweepy API connection"""

    # Logging
    logger = logging.getLogger()

    # Store your Twitter Developer accounts credentials here. This is needed to use the Tweepy API with your account.
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""


    # Uncomment this code if you would rather store your credentials in your local computers environment variables
    #consumer_key = os.getenv("CONSUMER_KEY")
    #consumer_secret = os.getenv("CONSUMER_SECRET")
    #access_token = os.getenv("ACCESS_TOKEN")
    #access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    print("API created")
    return api
