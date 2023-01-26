api_key = ''
client_secret = ''


def get_api_key():
    global api_key
    if api_key == '':
        with open('src/config/api_key.txt', 'r') as api_key_file:
            api_key = api_key_file.read()
    return api_key


def get_client_secret():
    global client_secret
    if client_secret == '':
        with open('src/config/client_secret.txt', 'r') as client_secret_file:
            client_secret = client_secret_file.read()
    return client_secret
