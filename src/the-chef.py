#!/usr/bin/python3

import discord
import logging
import argparse

from recipe import Recipe

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='the-chef.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!miam'):
        recipe = Recipe().fetch()
        await message.channel.send(str(recipe))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A discord bot fetching cooking recipes :p")
    parser.add_argument('--token', '-t', type=str, help='the bot access token', required=True)
    args = parser.parse_args()

    client.run(args.token)