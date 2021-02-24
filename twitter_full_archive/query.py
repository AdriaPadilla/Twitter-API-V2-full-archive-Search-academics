import requests

search_url = "https://api.twitter.com/2/tweets/search/all"

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def query(headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def query_loop(headers, query_params, pagination_token):
    query_params["next_token"] = pagination_token
    response = requests.request("GET", search_url, headers=headers, params=query_params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
