from Vidobot import Vidobot
import discord
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

vidobot = Vidobot()

discord.opus.load_opus("libopus.dylib")
if not discord.opus.is_loaded():
    print("Opus not loaded. Exiting...")
    exit(-1)
else:
    print("Opus loaded.")

with open("token", 'r') as f:
    token = f.read()
vidobot.run(token)
