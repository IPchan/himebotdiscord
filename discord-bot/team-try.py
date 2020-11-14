def teamallocation(rlist,l):
import discord
import random
import re
client = discord.Client()

p_list =[[],[],[],[],[],[]]
n_list =[]
name = ''

cmd_list =['!ad','!12','!list','!clear','!help']
position =['top','mid','adc','sup','jg','fill']


@client.event
async def on_ready():
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')


@client.event
async def on_message(message):
    if client.user == message.author:
        return

    global p_list
    global n_list
    global name

    cmd_1 = command(message.content)
    cmd_2 = command(message.content,1)
    cmd_3 = command(message.content,2)

    name = username(message.author)
    l_name = lolname(cmd_3)


    if cmd_1 == cmd_list[0]:#!ad
        if l_name in n_list:
            comment = l_name+'は既に登録されています'
        else:
            try:
                p = position.index(cmd_2)
            except ValueError:
                p = 5
            n_list +=[l_name]
            p_list[p] +=[l_name]
            comment = l_name+'の希望ポジションは'+position[p]+'です'


    elif cmd_1 == cmd_list[1]:#12
        if len(n_list) <=1:
            comment = '2人以上登録してください'
        else:
            n = teamlen(n_list)
            a_list = teamshuffle(p_list)
            comment = teamallocation(a_list,n)

    elif cmd_1 == cmd_list[2]:#list
        comment = sendlist(position,p_list)

    elif cmd_1 == cmd_list[3]:#clear
        if len(n_list) !=0:
            p_list =[[],[],[],[],[],[]]
            n_list =[]
            comment ='リストを空にしました'
        else:
            comment ='リストは空です'

    elif cmd_1 == cmd_list[4]:#help
        comment ='---------------------------------------------\n\
操作方法\n\
\n\
!ad (ポジション) (登録する名前) ※()内は省略可\n\
登録\n\
\n\
!12\n\
チーム分け\n\
\n\
!list\n\
リストを表示\n\
\n\
!clear\n\
リストを空にする\n\
---------------------------------------------'

    else:
        return


    await client.send_message(message.channel,comment)

#空白で区切られたメッセージのn番目を取り出す
def command(message,n =0):
    try:
        return message.split(' ')[n]
    except IndexError:
        return ''

#ユーザー名の後ろの#xxxxを消す
def username(user):
    s_user = str(user)
    return re.split('#',s_user)[0]

#リストに登録する名前
def lolname(user):
    if user != '':
        return user
    else:
        return name

#チーム数
def teamlen(men_list):
    n =(len(men_list)+4)//5
    if n >=2:
        return n
    else:
        return 2

#リストをシャッフルする
def teamshuffle(plist):
    random.shuffle(plist)
    result =[]
    for i in plist[5]:
        plist += [i]
    plist[5] =[]
    for x in plist:
        if type(x) == list:
            for user in x:
                result +=[user]
        else:
            result +=[x]
    return result

#チームを分ける
def teamallocation(rlist,l):
    result =[[]for i in range(l)]
    n =0
    for x in rlist:
        result[n] += [x]
        if n +1 == l:
            n =0
        else:
            n +=1

    bunsyou =''
    m =1
    for y in result:
        bunsyou +='チーム'+str(m)+'\n'
        for z in y:
            bunsyou +='['+ z +']'
        bunsyou +='\n\n'
        m +=1
    return bunsyou

#リストを表示
def sendlist(position,list):
    bunsyou =''
    for (x,y) in zip(position,p_list):
        if len(y) >=1:
            bunsyou += x +'\n'
            for z in y:
                bunsyou +='['+ z +']'
            bunsyou +='\n\n'
    return bunsyou



client.run('ここにトークンを入れる')
