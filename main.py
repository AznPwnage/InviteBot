import json
import pickle
import time
from enum import Enum

import requests
import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
guild = discord.Object(id=1066525478887899226)  # replace with your guild id
api_key = ''


class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


class OAuthToken:
    def __init__(self, access_token, token_type, expires_at_seconds, refresh_token, refresh_expires_at_seconds, membership_id):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_at_seconds = expires_at_seconds
        self.refresh_token = refresh_token
        self.refresh_expires_at_seconds = refresh_expires_at_seconds
        self.membership_id = membership_id


class GrantType:
    def __init__(self, name, code_type):
        self.name = name
        self.code_type = code_type


class Clans(Enum):
    Emerald = '3640796'
    Jade = '3892235'
    Peridot = '4381485'
    Beryl = '4381489'
    Ruby = '3759206'
    Garnet = '3893809'
    Thulite = '4382110'
    Onyx = '3893887'
    Diamond = '4315576'


class GrantTypes(Enum):
    AuthorizationCode = GrantType('authorization_code', 'code')
    RefreshToken = GrantType('refresh_token', 'refresh_token')


class MembershipTypes(Enum):
    Xbox = '1'
    PS = '2'
    Steam = '3'


intents = discord.Intents.default()
client = BotClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

    global api_key
    api_key = get_api_key()


@client.tree.command()
@app_commands.describe(
    name='Name of account',
    clan='Name of clan',
    code='Code copied from URL'
)
async def authorize(interaction: discord.Interaction, name: str, clan: Clans, code: str):
    """Authorize the bot to use your Bungie account"""

    try:
        response = call_oauth_token_api(code, GrantTypes.AuthorizationCode.value)
    except Exception:
        await interaction.response.send_message('Failed to authorize.')
        return

    oauth_token = convert_response_to_oauth_token(response.json())
    save_oauth_token(clan, oauth_token)

    await interaction.response.send_message('Authorized!')


@client.tree.command()
@app_commands.rename(bungie_name='bungie-name')
@app_commands.rename(membership_type='platform')
@app_commands.describe(
    bungie_name='Bungie Name of the user to invite (include the # and numbers)',
    membership_type='Platform',
    clan='Name of clan',
)
async def invite(interaction: discord.Interaction, bungie_name: str, membership_type: MembershipTypes, clan: Clans):
    """Invite a user to the clan"""
    try:
        oauth_token = get_oauth_token(clan)
    except Exception:
        await interaction.response.send_message('Unable to fetch token, please reauthenticate.')
        return

    try:
        membership_id = get_membership_id(bungie_name, membership_type.value)
    except Exception:
        await interaction.response.send_message('Unable to find membership id.')
        return

    try:
        send_invite(membership_type.value, membership_id, clan.value, oauth_token.access_token)
    except Exception:
        await interaction.response.send_message('Unable to send clan invite.')
        return

    await interaction.response.send_message('Invite sent!')


@client.tree.command()
@app_commands.rename()
async def test(interaction: discord.Interaction):
    """Test"""
    with open('Diamond', 'rb') as token_file:
        oauth_token = pickle.load(token_file)

    print(oauth_token.access_token)

    await interaction.response.send_message('Test complete.')


def convert_response_to_oauth_token(response_json):
    current_time = time.time()

    expires_at_seconds = current_time + response_json['expires_in']
    refresh_expires_at_seconds = current_time + response_json['refresh_expires_in']

    oauth_token = OAuthToken(response_json['access_token'],
                             response_json['token_type'],
                             expires_at_seconds,
                             response_json['refresh_token'],
                             refresh_expires_at_seconds,
                             response_json['membership_id'])
    return oauth_token


def get_oauth_token(clan: Clans):
    with open(clan.name, 'rb') as token_file:
        oauth_token = pickle.load(token_file)

    return handle_oauth_token(clan, oauth_token)


def save_oauth_token(clan: Clans, oauth_token: OAuthToken):
    with open(clan.name, 'wb') as token_file:
        pickle.dump(oauth_token, token_file)


def handle_oauth_token(clan: Clans, oauth_token: OAuthToken):
    current_time = time.time()

    if oauth_token.expires_at_seconds > current_time:
        return oauth_token

    response = call_oauth_token_api(oauth_token.refresh_token, GrantTypes.RefreshToken.value)

    oauth_token = convert_response_to_oauth_token(response.json())
    save_oauth_token(clan, oauth_token)

    return oauth_token


def call_oauth_token_api(code: str, grant_type: GrantType):
    url = 'https://www.bungie.net/platform/app/oauth/token/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    client_secret = get_client_secret()
    print(client_secret)
    body = {'grant_type': grant_type.name,
            grant_type.code_type: code,
            'client_id': '35375',
            'client_secret': client_secret}

    response = requests.post(url, headers=headers, data=body)
    if response.status_code != 200:
        raise Exception

    return response


def get_membership_id(bungie_name: str, membership_type: str):
    display_name, display_name_code = get_display_name_and_code(bungie_name)

    url = 'https://www.bungie.net/platform/destiny2/searchdestinyplayerbybungiename/' + membership_type
    headers = {'content-type': 'application/json', 'x-api-key': api_key}
    body = json.dumps({'displayName': display_name, 'displayNameCode': display_name_code})

    response = requests.post(url, headers=headers, data=body)
    if response.status_code != 200:
        raise Exception

    return response.json()['Response'][0]['membershipId']


def get_display_name_and_code(bungie_name: str):
    split_list = bungie_name.split('#', 1)
    if len(split_list[1]) != 4:
        raise Exception('Bungie name code is not of length 4')

    return split_list[0], split_list[1]


def get_api_key():
    with open('api_key.txt', 'r') as api_key_file:
        return api_key_file.read()


def get_client_secret():
    with open('client_secret.txt', 'r') as client_secret_file:
        return client_secret_file.read()


def send_invite(membership_type: str, membership_id: str, clan_id: str, access_token: str):
    url = 'https://www.bungie.net/platform/groupv2/' + clan_id + '/members/individualinvite/' + membership_type + '/' + membership_id
    authorization_value = 'Bearer ' + access_token
    headers = {'x-api-key': api_key, 'authorization': authorization_value, 'content-type': 'text/plain'}
    body = '{}'

    response = requests.post(url, headers=headers, data=body)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception

    return

client.run(token)
