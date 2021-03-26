import os
import json
import pandas as pd

import pymysql
from sqlalchemy import create_engine
from datetime import datetime

db_user = "Your DB USER"
db_password = "Your DB Password"
host = "¿Where is your DB? (localhost?)"
db_name = "The Database Name"
db_table = "Your DB Table" # If table doesn't exists, will create. If Exist, will append

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{host}/{db_name}?charset={charset}")
connection = pymysql.connect(host= host,
                             user= db_user,
                             password= db_password,
                             db= db_name,
                             charset= charset)

def save_data(json_response,counter,pharse):
    actual_time = datetime.now()
    data = json_response["data"]

    general_df = []

    for element in data:

        # Get the author name
        list_of_users = json_response["includes"]["users"]
        author_id = element["author_id"]
        for user in list_of_users:
            if user["id"] == author_id:
                username = user["username"]
            else:
                pass

        # Get Media Attributes
        media_duration = 0
        media_views = 0

        try:
            media_lists = element["attachments"]["media_keys"]
            media_meta = json_response["includes"]["media"]
            for media in media_lists:
                for media_attached in media_meta:
                    if media == media_attached["media_key"]:
                        media_type = media_attached["type"]
                        if media_type == "video":
                            ms_media_duration = media_attached["duration_ms"]
                            media_duration = ms_media_duration/1000
                            media_views = media_attached["public_metrics"]["view_count"]
                        else:
                            pass
                    else:
                        pass
        except KeyError:
            media_type = "false"

        # In Reply To ID
        try:
            reply = element["in_reply_to_user_id"]
        except KeyError:
            reply = "false"


            # Hashtag list
        try:
            entities = element["entities"]
            hastags = entities["hashtags"]
            hashtag_list = []
            for hastag in hastags:
                hash = hastag["tag"]
                hashtag_list.append(hash)
        except KeyError:
            hashtag_list = "false"

            # MENTIONS
        try:
            entities = element["entities"]
            mentions = entities["mentions"]
            mentions_list = []
            for mention in mentions:
                user = mention["username"]
                mentions_list.append(user)
        except KeyError:
            mentions_list = "false"

            # Anotations TYPE
        try:
            entities = element["entities"]
            anotations = entities["annotations"]
            anotations_type_list = []
            anotations_element_list = []
            for anotation in anotations:
                type = anotation["type"]
                anotations_type_list.append(type)
                text = anotation["normalized_text"]
                anotations_element_list.append(text)

        except KeyError:
            anotations_type_list = "false"
            anotations_element_list = "false"

        # GEO DATA

        try:
            geo = element["geo"]
            try:
                place_id = geo["place_id"]
                places = json_response["includes"]["places"]
                for place in places:
                    if place["id"] == place_id:
                        place_name = place["full_name"]
                    else:
                        pass
            except KeyError:
                place_id = "false"
                place_name = "false"
                pass
            try:
               coordinates = geo["coordinates"]["coordinates"]
            except KeyError:
                coordinates = "false"
                pass
        except KeyError:
            place_id = "false"
            coordinates = "false"
            place_name = "false"


        # Generate the Dataframe

        df = pd.DataFrame ({
            "retrieved_at": actual_time,
            "tweet_id": element["id"],
            "tweet_created_at": element["created_at"],
            "sensitive": element["possibly_sensitive"],
            "lang": element["lang"],
            "source": element["source"],
            "username": username,
            "user_id": element["author_id"],
            "text": element["text"],
            "in_reply_to_id": reply,
            "rt_count": element["public_metrics"]["retweet_count"],
            "reply_count": element["public_metrics"]["reply_count"],
            "like_count": element["public_metrics"]["like_count"],
            "quote_count": element["public_metrics"]["quote_count"],
            "has_media": media_type,
            "if_video_duration": media_duration,
            "if_video_views": media_views,
            "tweet_url": f"https://twitter.com/{username}/status/{element['id']}",
            "ent_hashtags": [hashtag_list],
            "ent_mentions": [mentions_list],
            "ent_anotation_types": [anotations_type_list],
            "ent_anotation_elements": [anotations_element_list],
            "place_id": place_id,
            "place_name": place_name,
            "coordinates": [coordinates],

        }, index=[0])

        general_df.append(df)

    counter_n = str(counter)

    final_df = pd.concat(general_df)
    capture_time = actual_time.strftime("%d-%m-%Y %H:%M:%S")
    captured_tweets = int(counter_n) * 500
    print(f"loop nº {counter_n} for {pharse} dumped to DB at {capture_time} - Captured Tweets: ({captured_tweets})")
    final_df.to_sql(db_table, index=False, con=engine, if_exists='append', chunksize=1000, method='multi')
