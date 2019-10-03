mongodb_config = {
    "username": "",
    "password": "",
    "database": "",
    "collection": "",
    "protocol": "mongodb+srv",
    "cluster": "",
    "urlParams": "retryWrites=true&w=majority",
}

file_config = {
    "path": "logs.log"
}

app_config = {
    # in seconds
    "loggingInterval": 60,

    # implemented:
    # MongoDBLogger / FileLogger / ConsoleLogger
    "logger": "ConsoleLogger",

    # endpoint
    "host": "127.0.0.1",
    "port": 1410
}

# Do not touch
mongodb_config["urlPattern"] = "{protocol}://{username}:{password}@{cluster}.mongodb.net/{database}?{urlParams}"
mongodb_config['url'] = mongodb_config['urlPattern'].format(**mongodb_config)