import os
import sys


def return_bad_keywords():
    """
    Bad keywords are used to make sure the tweet is ok to interact with.

    You need to create your own bad keywords. There are seperate lists for each item checked (username, bio, tweet text) because 
    checking all keywords against a twitter username or profile URL can filter out too many tweets.
    """
    try:
        # Bad keyword categories
        badKeywordsCategory1 = []
        badKeywordsCategory2 = []

        # Bad keywords used to filter
        badKeywordsTweetText = []
        badKeywordsUserBio = []
        badKeywordsUsername = []

        # Load bad keyword lists used to filter

        # badKeywords - TweetText
        badKeywordsTweetText.extend(badKeywordsCategory1)
        badKeywordsTweetText.extend(badKeywordsCategory2)

        # badKeywords - UserBio
        badKeywordsUserBio.extend(badKeywordsCategory1)
        badKeywordsUserBio.extend(badKeywordsCategory2)

    
        # badKeywords - Username
        badKeywordsUsername.extend(badKeywordsCategory1)
        badKeywordsUsername.extend(badKeywordsCategory2)

        return(badKeywordsTweetText, badKeywordsUserBio, badKeywordsUsername)
    except Exception as e:
        raise e