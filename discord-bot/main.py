import os
import traceback
import discord
from discord.ext import commands
from modules.grouping import MakeTeam
from dotenv import load_dotenv
import config
import datetime
#CONSUMER_KEY = os.environ["CONSUMER_KEY"]
#CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
#ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
#ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
bot = commands.Bot(command_prefix='hi?')

"起動処理"
@bot.event
async def on_ready():
  print('-----Logged in info-----')
  print(bot.user.name)
  print(bot.user.id)
  print('------------------------')

"コマンド"

"メンバーが均等"
@bot.command()
async def team(ctx, specified_num=2):
  make_team = MakeTeam()
  remainder_flag = 'true'
  msg = make_team.make_party_num(ctx,specified_num,remainder_flag)
  await ctx.channel.send(msg)


"人数が均等でない"
@bot.command()
async def team_norem(ctx,specified_num=2):
  make_team = MakeTeam()
  msg = make_team.make_party_num(ctx,specified_num)
  await ctx.channel.send(msg)

"メンバー数を指定してチーム分け"
@bot.command()
async def group(ctx, specified_num = 1):
  make_team = MakeTeam()
  msg = make_team.make_specified_len(ctx,specified_num)
  await ctx.channel.send(msg)

"時間計測"



client = discord.Client()
pretime_dict = {}

@client.event
async def on_voice_state_update(before, after):
  print("ボイスチャンネルで変化がありました")

  if((before.voice.self_mute is not after.voice.self_mute) or (before.voice.self_deaf is not after.voice.self_deaf)):
    print("ボイスチャンネルでミュート設定の変更がありました")
    return

  if(before.voice_channel is None):
    pretime_dict[after.name] = datetime.datetime.now()
  elif(after.voice_channel is None):
    duration_time = pretime_dict[before.name] - datetime.datetime.now()
    duration_time_adjust = int(duration_time.total_seconds()) * -1

    reply_channel_name = "勉強部屋"
    reply_channel = [channel for channel in before.server.channels if channel.name == reply_channel_name][0]
    reply_text = after.name + "　が　"+ before.voice_channel.name + "　から抜けました。　通話時間：" + str(duration_time_adjust) +"秒"

    await client.send_message(reply_channel ,reply_text)

"BOTとの接続と起動"
bot.run(TOKEN)
