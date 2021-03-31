import requests
import os
import json

bearer_token = "Your Bearer Token Here"
output_folder = "output/" # Output Json Folder

def create_url():

    usernames = "usernames=adriapadilla,monrodriguez" # 100 users Max, coma separated.

    # Avaliable User Fields: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
    user_fields = "user.fields=description,created_at,location,verified,public_metrics,protected" # Fields Here, coma separated.

    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

# Primer es genera la capçalera d'autorització per la consulta
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with open((output_folder + "user-ouptut.json"), 'w', encoding='utf-8') as f:
            json.dump(json_response, f, ensure_ascii=False, indent=4)
    except IndexError:
        print("ERROR")
        pass

if __name__ == "__main__":
    main()
