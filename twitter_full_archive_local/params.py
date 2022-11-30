def parameters(start_date, end_date, start_time, end_time, hashtag):
    query_params = {
        'start_time': f'{start_date}T{start_time}Z', # API DATE/HOUR FORMAT = YYYY-MM-DDTHH:MM:SSZ
        'end_time': f'{end_date}T{end_time}Z',
        'tweet.fields': 'author_id,created_at,in_reply_to_user_id,possibly_sensitive,public_metrics,lang,source,entities,geo,reply_settings,conversation_id',
        'max_results': 490,
        'expansions': 'attachments.media_keys,author_id,geo.place_id,referenced_tweets.id',
        'media.fields': 'duration_ms,media_key,url,type,public_metrics',
        'user.fields': 'username',
        }
    pharse = {"value": f"{hashtag}"}
    return query_params, pharse
