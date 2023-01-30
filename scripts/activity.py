import requests
import time
from datetime import datetime
import pandas as pd
import credentials as c
import json


search_url = "https://api.twitter.com/2/tweets/counts/all"
sleep_seconds = 3  # Sleep time in case of reach API limit

responses_list = []
final_frame = []

## dummy ##
next_token = "none"

def query(query_params, search_url):
    if query_params["next_token"] == "none":
        query_params.pop("next_token")
    else:
        pass
    api_response = requests.request("GET", search_url, auth=bearer_oauth, params=query_params, timeout=10)
    if api_response.status_code != 200:
        print(api_response.text)

    else:
        response = api_response.json()
        try:
            responses_list.append(response)
            next_token = response["meta"]["next_token"]
            print(next_token)
            query_params["next_token"] = next_token
            time.sleep(sleep_seconds)
            query(query_params, search_url)

        except KeyError:
            print("last token")
            print(len(responses_list))
            with open('mydata.json', 'w') as f:
                json.dump(responses_list, f)
            for item in responses_list:
                dfItem = pd.DataFrame.from_records(item["data"])
                final_frame.append(dfItem)
                print(dfItem)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {c.BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
    return r


def controller():

    jobs_list = pd.read_csv("capture_jobs.csv", sep=";")  # IMPORT THE JOBS LIST
    print(jobs_list)  # PRINT THE JOBS LIST

    # Starting the loop over the Jobs list
    for index, row in jobs_list.iterrows():

        # Compose de query parameters from CSV
        start_date = datetime.strptime(row["start"], "%d/%m/%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(row["end"], "%d/%m/%Y").strftime("%Y-%m-%d")
        start_time = row["start_time"]
        end_time = row["end_time"]
        hashtag = row["query"]

        query_params = {
        'query': f"{hashtag} -is:retweet",
        'start_time': f'{start_date}T{start_time}Z', # API DATE/HOUR FORMAT = YYYY-MM-DDTHH:MM:SSZ
        'end_time': f'{end_date}T{end_time}Z',
        'granularity': "day",
        'next_token': next_token
        }

        # QUery

        api_response = query(query_params, search_url)
        final = pd.concat(final_frame)
        total_tweets = final["tweet_count"].sum()
        final.to_csv(f"../datasets/count-{hashtag}-{start_date}-{end_date}-{total_tweets}.csv", sep=";", index=False)
        print("total tweets: "+str(final["tweet_count"].sum()))
controller()
