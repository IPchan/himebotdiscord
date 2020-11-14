import os
import traceback
import discord
from discord.ext import commands
from modules.grouping import MakeTeam

#CONSUMER_KEY = os.environ["CONSUMER_KEY"]
#CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
#ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
#ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


TOKEN = os.environ["DISCORD_BOT_TOKEN"] = 'Nzc0OTMyODI5NzM3ODQ0NzY3.X6e-cA.rxDVbIwGmRJdZXASAE4T4PT7Grk'
bot = commands.Bot(command_prefix='H?')

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

"BOTとの接続と起動"
bot.run(TOKEN)

#Nzc0OTMyODI5NzM3ODQ0NzY3.X6e-cA.rxDVbIwGmRJdZXASAE4T4PT7Grk
