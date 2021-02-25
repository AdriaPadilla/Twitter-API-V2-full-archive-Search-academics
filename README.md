# Twitter API V2 Full Archive Search for Academic Research

Here you will find a fully functional example of how "Search Tweets" Endpoint (Twitter API V2) works. You'll need:
- Access to the full [Twitter Archive for Academic Research](https://developer.twitter.com/en/solutions/academic-research)
- A Bearer Token (once your access is aproved, you'll need to create a new app and generate de Token).

## Before Using
Before using, please carefully read the documentation available on the twitter API V2. This is not intended to be a perfect example, but it can help you better understand how the API works, and how to perform queries taking advantage of the access level for researchers. There you will find answers to many of the questions you may have.

[Search Tweets READ THE DOCS](https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction)

## Dependencies
```bash
os
json
requests
Pandas
pymsql
sqlalchemy
```
## Setup
You'll need:
- Mysql database (recommend MariaDB or similar)
- Python3 installed
- Commandline interface (Windows/linux/MacOs terminals)

## Script workflow
launch with 
```
python3 main.py
```

- In params.py "pharses" variable, you can define the list of queries. You can use boolean operators [Building queries for Search Tweets](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)
- main For loop for each query.
- For query, dump response in MYSQL database with json_dumper.py config.
- If pagination token in results (will be presents if more than 500 results), get pagination token and iterate over the loop
- If pagination token is not in results, end for loop and start a new query.

## API RATE LIMITS
Twitter API V2, and more precisely, Twitter Full-archive search for Academic Research, have a rate limit of 300 request in a 15 min window. Please, don't change sleep times between queries. 
