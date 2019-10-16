mongodb_config = {
    "username": "",
    "password": "",
    "database": "",
    "collection": "",
    "protocol": "mongodb+srv",
    "cluster": "",
    "urlParams": "retryWrites=true&w=majority",
}

app_config = {
    # in seconds
    "loggingInterval": 10,

    # Enable or disable loggers
    "loggers": {
        "console": True,
        "mongodb": False,
        "file": True,
    },

    # choose main way to read data from
    # mongodb / file
    "main_data_source": "file",

    # endpoint
    "host": "0.0.0.0",
    "port": 9812
}

file_logger_config = {
    "path": "logs.log"
}

# Do not touch
mongodb_config["urlPattern"] = "{protocol}://{username}:{password}@{cluster}.mongodb.net/{database}?{urlParams}"
mongodb_config['url'] = mongodb_config['urlPattern'].format(**mongodb_config)