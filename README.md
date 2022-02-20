# Copeland_Tweepy_Twitter_Bot
This Python Twitter bot uses the Tweepy API to stream tweets. Tweets can then be filtered out if they contain undesirable properties or content, and tweets that pass inspection can be favorited or retweeted.

Instructions:<br>
Edit tweepy_bot_config.py with your Twitter developer account credentials<br>
Edit tweepy_bot_main.py with the keywords, hashtags and phrases you want to use for streaming tweets<br>
Edit tweepy_bot_unwanted_keywords.py with keywords, hashtags and phrases you want to filter out<br>


Streaming tweets:<br>
Use phrases, keywords or hash tags to determine which tweets you want to stream.<br>


Bot actions:<br>
Favorite tweets<br>
Retweet tweets<br>

Filter out unwanted tweets depending on the following properties:<br>
Picture<br>
URL included in tweet<br>
Tweet text<br>
Regular tweet vs retweet<br>
Possibly_sensative field<br>
Tweet age<br>
Tweet author bio<br>
Tweet author username<br>
Undesirable keyword: tweet text<br>
Undesirable keyword: authors bio<br>
Undesirable keyword: username<br>
Undesirable keyword: URL on authors profile<br>
Quote tweet<br>


Requirements:<br>
Twitter developer account - request one here https://developer.twitter.com/en/portal/petition/essential/basic-info <br>
Tweepy API - install with pip install tweepy <br>
Python 3.8+<br>

Resources:<br>
Tweepy API documentation - https://docs.tweepy.org/en/stable/ <br>
Tweepy tutorial - https://developer.twitter.com/en/docs/tutorials/how-to-create-a-twitter-bot-with-twitter-api-v2

Disclaimer:<br>
Twitter contains a large amount of filth. It's possible unwanted content can pass through the tweet quality inspections which is why it's vital to continously adapt your undesirable keywords list. Use at your own risk.
