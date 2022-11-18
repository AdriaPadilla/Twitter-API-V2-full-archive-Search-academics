import os
import json
import sys

from datetime import datetime


actual_time = datetime.now()

def save_data(json_response, loop_counter, filename, capture_name):
    output_folder = f"../datasets/{capture_name}/api_responses/"
    json_parsed = json_response.json()
    if json_parsed["meta"]["result_count"] == 0:
        print("no tweets")
        n_tweets = 0
        last_date = "no tweets"
        return n_tweets, last_date
    else:
        data = json_parsed["data"]

        n_tweets = len(data)
        last = data[-1]
        last_date = last["created_at"]

        counter_n = str(loop_counter)

        # THIS IS ONLY IF YOU WANT TO SAVE JSON PURE DATA. CREATES ONE JSON FILE FOR EACH LOOP.

        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            with open((output_folder + f"{filename}__loop-{counter_n}.json"), 'w', encoding='utf-8') as f:
                json.dump(json_parsed, f, ensure_ascii=False, indent=4)
                print(f"Loop {loop_counter} --> Dumped to JSON FILE {filename}")
            return n_tweets, last_date
        except IndexError:
            print("ERROR")
            pass
