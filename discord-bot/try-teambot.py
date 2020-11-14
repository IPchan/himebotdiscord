import discord
import pdb;
from discord.ext import commands
import random
TOKEN = ""


desc='''This is bot.
これはbotです'''

pdb.set_trace()
client = commands.bot(command_prefix = '!',description=desc)

@client.event
async def on_ready():
    print('Logget in as')
    print('BOT-NAME :',client.user.name)
    print('BOT-ID   :',client.user.id)
    print('-------')




@client.command()
async def command(team):
    return message.split(' ')[0]
cmd = command(message.content)
if cmd ==('team'):

@client.event
async def on_message(message):

    voice_channel = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
    p_list = voice_channel.voice_members

    for x in range(len(p_list)):
        print(p_list[x].display_name)




client.run("TOKEN")
