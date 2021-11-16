import os
import json

from datetime import datetime


actual_time = datetime.now()

def save_data(json_response, loop_counter, pharse, filename, capture_name):
    output_folder = f"{capture_name}/api_responses/"
    json_parsed = json_response.json()

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
