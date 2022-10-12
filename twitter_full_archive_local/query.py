import requests
import time
from datetime import datetime
from datetime import timedelta

# Notes
# There're a lot of print() in this file. This is made to keep a log/trace of what's happening
# during the development some bugs/problems where found. For example: when making API requests
# sometimes, randomly, the API freezes and there's no response, so I introduce a timeout=10 to make a retry
# Also, it's possible to reach the API rate limit despite the limitations.
# To deal with all this mess, I create a rudimentary "error control" and "print()" to monitor what is happening

search_url = "https://api.twitter.com/2/tweets/search/all"
sleep_seconds = 300  # Sleep time in case of reach API limit


def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers


def query(headers, params, pagination_token, loop_counter):
    if loop_counter == 1:
        print(f"Loop {loop_counter} --> making API REQUEST")
        api_response = requests.request("GET", search_url, headers=headers, params=params, timeout=10)
        return api_response

    if loop_counter != 1:
        print(f"Loop {loop_counter} --> making API REQUEST")
        params["next_token"] = pagination_token
        api_response = requests.request("GET", search_url, headers=headers, params=params, timeout=10)
        return api_response


def query_controller(headers, params, pagination_token, loop_counter):
    try:
        api_response = query(headers, params, pagination_token, loop_counter)

        # Controlling the API response
        if api_response.status_code == 200:
            print(f"Loop {loop_counter} --> API response OK")
            return api_response

        # DEAL WITH API RATE LIMITS
        if api_response.status_code != 200:
            print(f"Loop {loop_counter} --> API RESPONSE FAIL STATUS RESPONSE: {api_response.status_code}")

            # IF API LIMIT REACHED
            if api_response.status_code == 429:

                actual_time = datetime.now()
                capture_time = actual_time.strftime("%d/%m/%Y %H:%M:%S")
                sleeping_time = timedelta(seconds=sleep_seconds)
                retry_time = actual_time + sleeping_time

                print(
                    f"Loop {loop_counter} --> API LIMIT REACHED at {capture_time}. RETRY AT {retry_time.strftime('%d/%m/%Y %H:%M:%S')}")
                time.sleep(sleep_seconds)
                print(f"Loop {loop_counter} --> Retry request {headers} {params}")
                return query_controller(headers, params, pagination_token, loop_counter)  # Recursion in request
            
            # Handle Service Unavailable error 
            if api_response.status_code == 503:
                    actual_time = datetime.now()
                    capture_time = actual_time.strftime("%d/%m/%Y %H:%M:%S")
                    sleeping_time = timedelta(seconds=sleep_seconds)
                    retry_time = actual_time + sleeping_time

                    print(
                        f"Loop {loop_counter} --> Service Unavailable at {capture_time}. RETRY AT {retry_time.strftime('%d/%m/%Y %H:%M:%S')}")
                    time.sleep(sleep_seconds)
                    print(f"Loop {loop_counter} --> Retry request {headers} {params}")
                    return query_controller(headers, params, pagination_token, loop_counter)  # Recursion in request

            # When nothing works...
            else:
                raise Exception(api_response.status_code, api_response.text)

    # if timeout...
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        print(f"Loop {loop_counter} --> TIMEOUT! On {params} at {datetime.now()} Trying a RETRY ")
        return query_controller(headers, params, pagination_token, loop_counter)
