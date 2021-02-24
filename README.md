# Twitter Full-archive search for Academic Research

Here you will find a fully functional example of how "Search Tweets" Endpoint (Twitter API V2) works. You'll need:
- Access to the full [Twitter Archive for Academic Research](https://developer.twitter.com/en/solutions/academic-research)
- A Bearer Token (once your access is aproved, you'll need to create a new app and generate de Token).

## Before Using
Before using, please carefully read the documentation available on the twitter API V2. This is not intended to be a perfect example, but it can help you better understand how the API works, and how to perform queries taking advantage of the access level for researchers.



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
- Get params.py "pharses" variable, where you'll have defined at least one query.
- Get params.py "query_params" variable, where requested elements are defined.
- For loop for each query.
- For query, dump response in MYSQL database with json_dumper.py config.
- If pagination token in results (will be presents if more than 500 results), get pagination token and iterate over the loop
- If pagination token is not in results, end for loop and start a new query.


## API RATE LIMITS
Twitter API V2, and more precisely, Twitter Full-archive search for Academic Research, have a rate limit of 300 request in a 15 min window.


