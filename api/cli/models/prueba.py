from decouple import config

DB_CONNSTR = config("DB_CONNSTR")
URL = config("URL")

print(DB_CONNSTR)
print(URL)