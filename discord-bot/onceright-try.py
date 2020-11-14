import discord
client = discord.Client()

TOKEN = "ご自身のトーーーークン"

# 各ユーザのリアクション(スタンプ)を保存して置くためのdict
from collections import defaultdict
user_reaction_dic = defaultdict(dict)

# リアクションが追加された時の処理
@client.event
async def on_reaction_add(reaction, user):

    # リアクションが追加されたメッセージの取得
    message = reaction.message

    # この投稿に対してこれまでにリアクションしたかを判定
    if message.id not in user_reaction_dic[user.id]:
        # 新しく登録された絵文字なので情報を保存しておく
        user_reaction_dic[user.id][message.id] = reaction.emoji
    else:
        # 前回の絵文字を削除して更新する
        await client.remove_reaction(message, user_reaction_dic[user.id][message.id], user)
        user_reaction_dic[user.id][message.id] = reaction.emoji

# リアクションが削除された時の処理
@client.event
async def on_reaction_remove(reaction, user):

    # リアクションが追加されたメッセージの取得
    message = reaction.message

    # 保存してあるリアクション情報と一致したらそれを削除しておく
    if user_reaction_dic[user.id][message.id] == reaction.emoji:
        del user_reaction_dic[user.id][message.id]

# BOTを実行
client.run(TOKEN)
