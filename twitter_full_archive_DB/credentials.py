# TWITTER API CREDENTIALS
BEARER_TOKEN = "YOUR_BEARER_TOKEN" # Your Twitter Bearer Token Credential string

# DATABASE LOCATION AND CREDENTIALS
db_user = "your_db_user"  # Caution: same user can't write in multiple DB, use an exclusive user
db_password = "your_db_pw"
host = "localhost"  # Localhost if local DB, or ip to external. Can use Amazon RDS.
db_name = "db_name"
db_table = "table_name"  # If table doesn't exists, will create. If Exist, will append