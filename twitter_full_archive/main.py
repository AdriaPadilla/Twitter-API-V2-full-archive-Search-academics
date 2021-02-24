from params import query_params, pharses
import query as q
import json_dumper as dumper
import time

bearer_token = "YOUT ACADEMIC BEARER TOKEN HERE"

loop_counter = 1

def loop(headers, query_params, pagination_token, loop_counter):
    json_response = q.query_loop(headers, query_params, pagination_token)
    dumper.save_data(json_response, loop_counter, pharse)
    try:
        if json_response["meta"]["next_token"]:
            pagination_token = json_response["meta"]["next_token"] # New API V2 require pagination for each 500 results. Here we get the pagination token.
            time.sleep(4)  # THIS AVOID HIT RATE LIMIT (300 Requests in a 15 Min Window)
            print("sleeping for 4 sec")
            loop_counter += 1
            loop(headers, query_params, pagination_token, loop_counter)
    except KeyError:
        print("Last Page")

def main(loop_counter, pharse):
    headers = q.create_headers(bearer_token)
    query_params["query"] = pharse
    json_response = q.query(headers, query_params)
    dumper.save_data(json_response, loop_counter, pharse)
    try:
        if json_response["meta"]["next_token"]:
            pagination_token = json_response["meta"]["next_token"]
            loop_counter += 1
            time.sleep(4) # THIS AVOID HIT RATE LIMIT (300 Requests in a 15 Min Window)
            print("sleeping for 4 sec")
            loop(headers, query_params, pagination_token, loop_counter)
    except KeyError:
        print("Last Page")

if __name__ == "__main__":

      for pharse in pharses:
        pharse = pharse["value"]
        main(loop_counter, pharse)

