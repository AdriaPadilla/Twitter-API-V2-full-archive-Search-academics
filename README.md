# Twitter for Academic Research

## Introduction

Here you will find a fully functional example of how "Search Tweets" Endpoint (Twitter API V2) works. To make it work, you'll need:
- Access to the full [Twitter Archive for Academic Research](https://developer.twitter.com/en/solutions/academic-research)
- A Bearer Token (once your access is aproved, you'll need to create a new app and generate the Bearer Token).

## Versions
I created two versions for the same script:
- **DataBase version**: Will dump all data from the Twitter API to a MySQL/MariaDB database. 
- **Local Version**: Will create a .json file for each loop (500 tweets per loop). When all data is downloaded, the script generates a .csv pharsing all .json files downloaded.

### What version should I use ?
Some data requests could be extensive and intensive, resulting in large datasets and long waiting times (hours). Choose the local version if you're going to do a selective download. Also, keep in mind: after data request (that will be stored in .Json), your system need to process these files to generate the final dataset in .csv format. This process can be RAM intensive. If you are going to make large requests, I'ld recommend you using the database version, since data from API is dumped directly to MySql/MariaDB, avoiding JSON files.


## Before Using
Before using, please carefully read the documentation available on the twitter API V2. This is not intended to be a perfect example, but it can help you better understand how the API works, and how to perform queries taking advantage of the access level for researchers. There you will find answers to many of the questions you may have.

[Search Tweets READ THE DOCS](https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction)

## Possible Dependencies
```bash
os
json
requests
Pandas
Openyxl # For xlsx datasets
pymsql # Only For DB Version
sqlalchemy  # Only For DB Version
```
## Setup
You'll need:
- Python3 installed
- Commandline interface (Windows/linux/MacOs terminals)
- Recommend PyCharm IDE or similar, with virtual enviroments.

if you use DB version, you'll need a local or cloud MySQL/MariaDB. Also: user and credentials to access and dump the data.

**Define credentials (credentials.py)**
Copy/Paste your Twitter API Bearer Token in credentials.py
If you use DB version, you'll need to define DB username, password and table names in the same file.

## workflow
### 1. Define Search jobs in capture_jobs.csv
You can define one or **multiple searchs** (one row per search). The script will iterate over the file to search tweets within parameters.
| start | start_time | end | end_time | query |
|---|---|---|---|---|
| dd-mm-yyyy | HH:MM:SS | dd-mm-yyyy | HH:MM:SS | from:username or #hashtag |

**Example 1**
| start | start_time | end | end_time | query |
|---|---|---|---|---|
| 01-01-2021 | 15:00:00 | 15-01-2021 | 21:00:00 | from:adriapadilla |

will search all tweets between 1st january at 15pm to 15th january at 21pm from user adriapadilla

**Example 2**
| start | start_time | end | end_time | query |
|---|---|---|---|---|
| 01-01-2021 | 15:00:00 | 15-01-2021 | 21:00:00 | #UCL |
| 01-01-2020 | 15:00:00 | 15-01-2020 | 21:00:00 | #Another_hashtag |

will search all tweets between 1st january at 15pm to 15th january at 21pm with hashtag #UCL published in 2021. After that will make another search for the second line.

**OUTPUT FOLDER** 
Define output folder in "capture_name" field

### 2. Launch the script 
In terminal:
```
python3 main.py
```

## API RATE LIMITS
Twitter API V2, and more precisely, Twitter Full-archive search for Academic Research, have a rate limit of 300 request in a 15 min window. Please, don't change sleep times between queries. 

## Handling errors

During execution, the API query, or when parsing the data, various errors can occur. The script contains the following error handling:
- Request too many requests to the API
- API Timeout
- Empty API responses
- ### Known Errors:
- On big extractions: Native Python3 Recursion limit to 1000 loops. Then recursion limit error. This may occur near 500k tweets retrieved.

### Updates log:
- 06/11/2021: add "In_reply_to_username" in output .csv file for local version.

### Working on:
- Equalize code betweet versions.




