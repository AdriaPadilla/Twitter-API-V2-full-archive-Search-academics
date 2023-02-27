import glob
import pandas as pd
import json
from datetime import datetime
from tqdm import tqdm

output_folder = "output/"
actual_time = datetime.now()

global_frame = []

def extractor(file, works, position, hashtag):
    with open(file, encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

        if data["meta"]["result_count"] == 0:
            print("No results")
            return "empty"
        else:
            tweets = data["data"]

            general_df = []

            for element in tweets:
                try:
                    # Get the author name
                    list_of_users = data["includes"]["users"]
                    author_id = element["author_id"]
                    for user in list_of_users:
                        if user["id"] == author_id:
                            username = user["username"]
                            name = user["name"]
                            followers = user["public_metrics"]["followers_count"]
                            following = user["public_metrics"]["following_count"]
                            total_tweets = user["public_metrics"]["tweet_count"]
                            listed_count = user["public_metrics"]["listed_count"]
                        else:
                            username = "None"
                            name = "None"
                            followers = "None"
                            following = "None"
                            total_tweets = "None"
                            listed_count = "None"

                    # Get Media Attributes
                    media_duration = 0
                    media_views = 0

                    try:
                        media_lists = element["attachments"]["media_keys"]
                        media_meta = data["includes"]["media"]

                        # Multiple media elements in a single tweet need to place each element in a list and output them in the same cell.
                        media_type_list = []
                        media_url_list = []


                        for media in media_lists:
                            for media_attached in media_meta:
                                if media == media_attached["media_key"]:
                                    media_type = media_attached["type"]
                                    media_type_list.append(media_type)
                                    if media_type == "photo":
                                        media_url = media_attached["url"]
                                        media_url_list.append(media_url)
                                    else:
                                        media_url = "None"
                                        media_url_list.append(media_url)

                                    if media_type == "video":
                                        ms_media_duration = media_attached["duration_ms"]
                                        media_duration = ms_media_duration / 1000
                                        media_views = media_attached["public_metrics"]["view_count"]
                                    else:
                                        ms_media_duration = "None"
                                        media_duration = "None"
                                        media_views = "None"

                    except KeyError:
                        media_type_list = ["false"]
                        media_url_list = ["false"]

                    # In Reply To ID
                    reply_to_name = "false"
                    try:
                        reply_to_id = element["in_reply_to_user_id"]
                        entities = element["entities"]
                        mentions = entities["mentions"]
                        for mention in mentions:
                            if reply_to_id == mention["id"]:
                                reply_to_name = mention["username"]
                                profile = reply_to_name
                            else:
                                reply_to_name = "None"
                    except KeyError:
                        reply_to_id = "false"
                        reply_to_name = "false"
                        profile = username

                    # Reply Settings
                    try:
                        reply_setting = element["reply_settings"]
                        reply_setting = str(reply_setting)
                    except KeyError:
                        reply_setting = "false"

                    # Conversation ID
                    try:
                        conversation_id = element["conversation_id"]
                    except KeyError:
                        conversation_id = "false"

                    # Get entities

                    # Hashtag list
                    try:
                        entities = element["entities"]
                        hastags = entities["hashtags"]
                        hashtag_list = []
                        for hastag in hastags:
                            hash = hastag["tag"]
                            hashtag_list.append(hash)
                            hashtags_string = ";".join(hashtag_list)
                    except KeyError:
                        hashtags_string = "false"

                    ###################
                    ## TYPE OF TWEET ##
                    ###################

                    # What kind of tweet is?
                    try:
                        tweet_type = element["referenced_tweets"][0]["type"]
                    except KeyError:
                        tweet_type = "original"

                    try:
                        referenced_tweets = element["entities"]["urls"][0]["expanded_url"]
                    except KeyError:
                        try:
                            referenced_tweets = f"https://twitter.com/{reply_to_name}/status/{element['referenced_tweets'][0]['id']}"
                        except KeyError:
                            referenced_tweets = "None"

                    # MENTIONS

                    try:
                        entities = element["entities"]
                        mentions = entities["mentions"]
                        mentions_list = []
                        for mention in mentions:
                            user = mention["username"]
                            mentions_list.append(user)
                            mentions_string = ";".join(mentions_list)
                    except KeyError:
                        mentions_string = "false"

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
                            annotations_type_string = ";".join(anotations_type_list)
                            annotations_elements_string = ";".join(anotations_element_list)

                    except KeyError:
                        annotations_type_string = "false"
                        annotations_elements_string = "false"

                    # GEO DATA

                    try:
                        geo = element["geo"]
                        try:
                            place_id = geo["place_id"]
                            places = data["includes"]["places"]
                            for place in places:
                                if place["id"] == place_id:
                                    place_name = place["full_name"]
                                else:
                                    place_name = "None"
                        except KeyError:
                            place_id = "false"
                            place_name = "false"

                        try:
                            coordinates = geo["coordinates"]["coordinates"]
                            list_lat_lon = []
                            for coordinate in coordinates:
                                coord_string = str(coordinate)
                                list_lat_lon.append(coord_string)
                            coordinates_string = ";".join(list_lat_lon)
                        except KeyError:
                            coordinates_string = "false"

                    except KeyError:
                        place_id = "false"
                        coordinates_string = "false"
                        place_name = "false"

                    # Get Year
                    year = element["created_at"].split("-")[0]



                    # Generate the Dataframe
                    df = pd.DataFrame({
                        "retrieved_at": actual_time,
                        "query": hashtag,
                        "tweet_created_at": element["created_at"],
                        # "tweet_year": year,
                        "tweet_url": f"https://twitter.com/{username}/status/{element['id']}",
                        "tweet_id": element["id"],
                        "tweet_type":tweet_type,
                        "in_reply_to_name": reply_to_name,
                        "referenced_tweets": referenced_tweets,
                        "sensitive": element["possibly_sensitive"],
                        "lang": element["lang"],
                        # "source": element["source"],
                        "username": username,
                        "user_id": element["author_id"],
                        "text": element["text"],
                        # "reply_setting": reply_setting,
                        # "in_reply_to_id": reply_to_id,
                        # "in_reply_to_message": in_reply_to_message,
                        #"conversation": f"https://www.twitter.com/{profile}/status/{conversation_id}",
                        "rt_count": element["public_metrics"]["retweet_count"],
                        "reply_count": element["public_metrics"]["reply_count"],
                        "like_count": element["public_metrics"]["like_count"],
                        "quote_count": element["public_metrics"]["quote_count"],
                        "has_media": [media_type_list],
                        "if_video_duration": media_duration,
                        "if_video_views": media_views,
                        "media_url": [media_url_list],
                        "ent_hashtags": hashtags_string,
                        "ent_mentions": mentions_string,
                        "ent_anotation_types": annotations_type_string,
                        "ent_anotation_elements": annotations_elements_string,
                        #"place_id": place_id,
                        "place_name": place_name,
                        "visible_user_name": name,
                        "followers_count": followers,
                        "following_count": following,
                        "user_total_tweets": total_tweets,
                        "listed_on": listed_count,
                        # "coordinates": coordinates_string,
                    }, index=[0])

                    general_df.append(df)
                except(KeyError, IndexError):
                    pass

            final_df = pd.concat(general_df)

            return final_df

def crontroller(filename, hashtag, capture_name):
    files = glob.glob(f"../datasets/{capture_name}/api_responses/{filename}*.json")
    print(files)
    works = len(files)
    for file in tqdm(files, desc="Pharsing JSON files..."):
        position = files.index(file)
        dataframe = extractor(file, works, position, hashtag)
        global_frame.append(dataframe)
    print("Creating df...")
    try:
        export_frame = pd.concat(global_frame)
        print("exporting df")
        export_frame.to_csv(f"../datasets/{capture_name}/dataset-{filename}.csv", index=False, sep=",",quotechar='"', line_terminator="\n")
        print("Done!")
        global_frame.clear()
    except (ValueError, TypeError):
        print("Nothing to Export")
        pass
