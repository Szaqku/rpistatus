mongodb_config = {
    "username": "",
    "password": "",
    "database": "",
    "collection": "",
    "protocol": "mongodb+srv",
    "cluster": "",
    "urlParams": "retryWrites=true&w=majority",
    "urlPattern": "{protocol}://{username}:{password}@{cluster}.mongodb.net/{database}?{urlParams}"
}

app_config = {
    # in seconds
    "loggingInterval": 60,

    # implemented:
    # MongoDBLogger / FileLogger
    "logger": "FileLogger"
}

# Do not touch
mongodb_config['url'] = mongodb_config['urlPattern'].format(**mongodb_config)