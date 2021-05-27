from params import query_params, pharses
import query as q
import json_dumper as dumper
import network as gr

import time
import pandas as pd
from datetime import datetime

bearer_token = "Your Bearer Token"

loop_counter = 1

global_df = []

def loop(headers, query_params, pagination_token, loop_counter):
    print("data from page: "+str(loop_counter))
    json_response = q.query_loop(headers, query_params, pagination_token)
    df = dumper.save_data(json_response, loop_counter, pharse)
    global_df.append(df)
    try:
        if json_response["meta"]["next_token"]:
            pagination_token = json_response["meta"]["next_token"]
            time.sleep(4)
            loop_counter += 1
            loop(headers, query_params, pagination_token, loop_counter)
    except KeyError:
        print("Last Page")

def main(loop_counter, pharse):
    headers = q.create_headers(bearer_token)
    query_params["query"] = pharse
    json_response = q.query(headers, query_params)
    df = dumper.save_data(json_response, loop_counter, pharse)
    global_df.append(df)
    try:
        if json_response["meta"]["next_token"]:
            pagination_token = json_response["meta"]["next_token"]
            loop_counter += 1
            time.sleep(4)
            loop(headers, query_params, pagination_token, loop_counter)
    except KeyError:
        print("Last Page")

if __name__ == "__main__":

    for pharse in pharses:
        pharse = pharse["value"]
        print(pharse)

        main(loop_counter, pharse)
        print("creating final Dataframe")
        final_frame = pd.concat(global_df)
        print("creating graph files")
        gr.graph(final_frame)

        actual_time = datetime.now()
        capture_time = actual_time.strftime("%d-%m-%Y-%H-%M-%S")
        print("saving data in excel file")
        final_frame.to_excel(f"{capture_time}-ouptut.xlsx")
