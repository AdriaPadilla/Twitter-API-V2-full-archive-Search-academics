import credentials as c
import params as p
import query as q
import json_dumper as dumper
import json_parser as par

import time
import os
import pandas as pd
from datetime import datetime

### Counters and Dummy variables ###
loop_counter = 1  # Set loop counter to 1
sleeper = 6  # Alert! MAX 300 queries in 15 min window or 1 query/s
total_tweets = 0 # Number of tweets downloaded
maximum_tweets = 1000000 # Max Tweets to download
####################################

### SET RECURSION LIMIT ####
import sys
sys.setrecursionlimit(round(maximum_tweets/450))
print(sys.getrecursionlimit())

### END RECURSION LIMIT ###


def loop(headers, query_params, pagination_token, loop_counter, filename, total_tweets, capture_name):
    json_response = q.query_controller(headers, query_params, pagination_token, loop_counter)
    n_tweets, last_date = dumper.save_data(json_response, loop_counter, filename, capture_name)
    total_tweets = n_tweets + total_tweets
    actual_time = datetime.now()
    print(f"Loop {loop_counter} --> {query_params['query']} from {query_params['start_time']} to {query_params['end_time']} dumped to JSON at {actual_time}")
    print(f"Loop {loop_counter} --> Total Tweets downladed: " + str(total_tweets)+f" | Last date: {last_date}")
    try:
        if json_response.json()["meta"]["next_token"]:
            pagination_token = json_response.json()["meta"]["next_token"]
            time.sleep(sleeper)
            loop_counter += 1
            loop(headers, query_params, pagination_token, loop_counter, filename, total_tweets, capture_name)
    except KeyError:
        print("Last Page")


def main(loop_counter, total_tweets):

    jobs = pd.read_csv("capture_jobs.csv", sep=";")  # IMPORT THE JOBS LIST
    print(jobs)  # PRINT THE JOBS LIST

    # Starting the loop over the Jobs list
    for index, row in jobs.iterrows():
        # Compose de query parameters from CSV
        start_date = datetime.strptime(row["start"], "%d/%m/%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(row["end"], "%d/%m/%Y").strftime("%Y-%m-%d")
        start_time = row["start_time"]
        end_time = row["end_time"]
        hashtag = row["query"]
        capture_name = row["capture_name"]

        # create the query string
        query_params, pharse = p.parameters(start_date, end_date, start_time, end_time, hashtag)
        pharse = pharse["value"]
        query_params["query"] = pharse

        # Create the output name
        try:
            if not os.path.exists(f"datasets/{capture_name}"):
                os.makedirs(f"datasets/{capture_name}")
        except IndexError:
            print("ERROR")
            pass

        # Generate the Filename
        actual_time = datetime.now()
        capture_time = actual_time.strftime("%d-%m-%Y-%H-%M-%S")
        filename = (f"{pharse}__at_{capture_time}__from_{start_date}__to__{end_date}").replace(":", "-")

        # Generate APP Auth
        headers = q.create_headers(c.BEARER_TOKEN)


        # Start Extraction
        pagination_token = None
        json_response = q.query_controller(headers, query_params, pagination_token, loop_counter)
        n_tweets, last_date = dumper.save_data(json_response, loop_counter, filename, capture_name)
        total_tweets = n_tweets + total_tweets

        actual_time = datetime.now()
        print(f"Loop {loop_counter} --> Query {loop_counter} | {query_params['query']} from {query_params['start_time']} to {query_params['end_time']} dumped to JSON at {actual_time}")
        print(f"Loop {loop_counter} --> Total Tweets downladed: " + str(total_tweets)+f" | Last date: {last_date}")

        try:
            if json_response.json()["meta"]["next_token"]:
                pagination_token = json_response.json()["meta"]["next_token"]
                loop_counter += 1
                time.sleep(sleeper)
                loop(headers, query_params, pagination_token, loop_counter, filename, total_tweets, capture_name)
        except KeyError:
            print(f"Last Page for {query_params}")

        # Sleeping 10 second between jobs to avoid reach API limits
        print("sleeping 10 secs between jobs")

        # CREATING DATAFRAMES

        par.crontroller(filename, hashtag, capture_name)
        print("Sleeping 10 Seconds")
        time.sleep(10)

if __name__ == "__main__":
    main(loop_counter, total_tweets)

