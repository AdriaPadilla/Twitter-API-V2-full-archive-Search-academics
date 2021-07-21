import credentials as c
import params as p
import query as q
import json_dumper as dumper
import json_parser as par

import time
import pandas as pd
from datetime import datetime

loop_counter = 1  # Set loop counter to 1
sleeper = 5  # Alert! MAX 300 queries in 15 min window or 1 query/s

def loop(headers, query_params, pagination_token, loop_counter, filename):
    json_response = q.query_controller(headers, query_params, pagination_token, loop_counter)
    dumper.save_data(json_response, loop_counter, pharse, filename)
    actual_time = datetime.now()
    print(f"Loop {loop_counter} --> {query_params['query']} from {query_params['start_time']} to {query_params['end_time']} dumped to db at {actual_time}")

    try:
        if json_response.json()["meta"]["next_token"]:
            pagination_token = json_response.json()["meta"]["next_token"]
            time.sleep(sleeper)
            loop_counter += 1
            loop(headers, query_params, pagination_token, loop_counter, filename)
    except KeyError:
        print("Last Page")


def main(loop_counter, query_params, filename):
    headers = q.create_headers(c.BEARER_TOKEN)
    pagination_token = None
    json_response = q.query_controller(headers, query_params, pagination_token, loop_counter)
    dumper.save_data(json_response, loop_counter, pharse, filename)
    actual_time = datetime.now()
    print(f"Loop {loop_counter} --> Query {loop_counter} | {query_params['query']} from {query_params['start_time']} to {query_params['end_time']} dumped to db at {actual_time}")

    try:
        if json_response.json()["meta"]["next_token"]:
            pagination_token = json_response.json()["meta"]["next_token"]
            loop_counter += 1
            time.sleep(sleeper)
            loop(headers, query_params, pagination_token, loop_counter, filename)
    except KeyError:
        print(f"Last Page for {query_params}")


if __name__ == "__main__":

    dates_list = pd.read_csv("capture_jobs.csv", sep=";")  # IMPORT THE JOBS LIST
    print(dates_list)  # PRINT THE JOBS LIST

    # Starting the loop over the Jobs list
    for index, row in dates_list.iterrows():
        # Compose de query parameters from CSV
        start_date = datetime.strptime(row["start"], "%d/%m/%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(row["end"], "%d/%m/%Y").strftime("%Y-%m-%d")
        start_time = row["start_time"]
        end_time = row["end_time"]
        hashtag = row["query"]

        # create the query string
        query_params, pharse = p.parameters(start_date, end_date, start_time, end_time, hashtag)
        pharse = pharse["value"]
        query_params["query"] = pharse

        # Generate the Filename
        actual_time = datetime.now()
        capture_time = actual_time.strftime("%d-%m-%Y-%H-%M-%S")
        filename = (f"{pharse}__at_{capture_time}__from_{start_date}__to__{end_date}").replace(":", "-")

        # Start the extraction
        main(loop_counter, query_params, filename)

        # Sleeping 10 second between jobs to avoid reach API limits
        print("sleeping 10 secs between jobs")

        # CREATING DATAFRAMES

        par.crontroller(filename)
        print("Sleeping 10 Seconds")
        time.sleep(10)

