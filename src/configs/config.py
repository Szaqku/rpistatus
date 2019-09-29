mongodb_config = {
    "username": "",
    "password": "",
    "database": "",
    "collection": "",
    "protocol": "mongodb+srv",
    "cluster": "",
    "urlParams": "retryWrites=true&w=majority",
    "urlPattern": "{protocol}://{username}:{password}@{cluster}.mongodb.net/{database}?{urlParams}",
    "url": ""
}

mongodb_config['url'] = mongodb_config['urlPattern'].format(**mongodb_config)

app_config = {
    # in seconds
    "loggingInterval": 60
}
