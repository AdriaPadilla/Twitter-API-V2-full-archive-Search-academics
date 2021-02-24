query_params = {
    'start_time': '2021-02-04T00:00:00Z', # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    'end_time': '2021-02-10T00:00:00Z', # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    'tweet.fields': 'author_id,created_at,in_reply_to_user_id,possibly_sensitive,public_metrics,lang,source',
    'max_results': 500, #This is the max results admited by API endpoint
    'expansions': 'attachments.media_keys,author_id',
    'media.fields': 'duration_ms,media_key,url,type,public_metrics',
    'user.fields': 'username',
    }

# This is an example of multiple queries in same work. 

pharses = [
    {"value": "#Buccaneers -is:retweet"}, # This will retreieve all Tweets with this exact hashtag, and will descard retweets.
    {"value": "from:Buccaneers"}, # This will retreieve all Tweets From Bucaneers account, including retweets.

    ]
