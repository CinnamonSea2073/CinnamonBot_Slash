import discord
from discord import Option
import os
from dotenv import load_dotenv
import aiohttp
import requests
import os
import time
import re
import queue
import asyncio
from mcipc.rcon.je import Client   
import yaml
import random
from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = discord.Bot()
GUILD_IDS = [879288794560471050]  # ← BOTのいるサーバーのIDを入れます


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


@bot.slash_command(description="あなたの名前か入力した名前に挨拶します", guild_ids=GUILD_IDS)
async def hello(
    ctx: discord.ApplicationContext,
    name: Option(str, required=False, description="名前を入力してね", )
):
    if not name:
        name = ctx.author
    await ctx.respond(f"こんにちは！ {name} さん！")


@bot.slash_command(description="しなもんにメンションを爆撃します", guild_ids=GUILD_IDS)
async def mention(
    ctx: discord.ApplicationContext,
    contents: Option(str, required=False, description="しなもんに爆撃したい内容を書いてね", )
):
    if not contents:
        contents = ctx.author
    await ctx.respond(f"<@698127042977333248> {contents} ")


@bot.slash_command(description="Embedのテスト", guild_ids=GUILD_IDS)
async def embedtest(
    ctx: discord.ApplicationContext,
    contents: Option(str, required=False, description="とめいとぅ", )
):
    if not contents:
        contents = ctx.author
    embed = discord.Embed( # Embedを定義する
                          title="しなもんサーバー開けやがれ",# タイトル
                          color=0x1e90ff, # フレーム色指定(今回は緑)
                          description="<@698127042977333248>", # Embedの説明文 必要に応じて
                          
                          )

    embed.set_footer(text="made by CinnamonSea2073", # フッターには開発者の情報でも入れてみる
                     icon_url="https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png")

    await ctx.respond(embed=embed)


@bot.slash_command(description="MCIDから顔面を生成っ！", guild_ids=GUILD_IDS)
async def face(
    ctx: discord.ApplicationContext,
    mcid: Option(str, required=True, description="マイクラIDをかいてね", )
):
    if not mcid:
        mcid = ctx.author
    mojang = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{mcid}").json()
    isvalid = mojang.get("id",None)
    if isvalid is None:
        await ctx.respond("プレイヤー'{}'は存在しません。".format(mcid))
    else:
        crafatar = requests.get(f"https://crafatar.com/avatars/{mojang['id']}", stream=True)
        with open(f"{mcid}.png", "wb") as f:
            f.write(crafatar.content)
        file = discord.File(f"{mcid}.png", filename=f"{mcid}.png")
        embed = discord.Embed(title=f"{mcid} のお顔")
        embed.set_image(url=f"attachment://{mcid}.png")
        await ctx.respond(file=file,embed=embed)
        os.remove(f"{mcid}.png")


@bot.slash_command(description="寝ろ", guild_ids=GUILD_IDS)
async def gotobed(
    ctx: discord.ApplicationContext,
):
    await ctx.respond(f":thinking::right_facing_fist::boom::bed:")


@bot.slash_command(description="整地から逃げるな(ほぼ自分用)", guild_ids=GUILD_IDS)
async def seichi(
    ctx: discord.ApplicationContext,
    contents: Option(str, required=False, description="しなもんに整地させたい内容を書いてね", )
):
    if not contents:
        contents = "整地から逃げるな"
    embed = discord.Embed( # Embedを定義する
                          title="整地から逃げるな",# タイトル
                          color=0x1e90ff, # フレーム色指定(今回は緑)
                          description="整地から逃げるな<@698127042977333248>", # Embedの説明文 必要に応じて
                          
                          )

    embed.add_field(name="JMS投票しよう（日課）",value="https://minecraft.jp/servers/54d3529e4ddda180780041a7")
    embed.add_field(name="monocraft投票しよう（日課）",value="https://monocraft.net/servers/Cf3BffNIRMERDNbAfWQm/vote")
    embed.add_field(name="サイト",value="https://www.seichi.network/gigantic")

    embed.set_footer(text="made by CinnamonSea2073", # フッターには開発者の情報でも入れてみる
                     icon_url="https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png")

    await ctx.respond(f"<@698127042977333248> {contents} ")
    await ctx.respond(embed=embed)


@bot.slash_command(description="品鯖にコマンドを送りつけます（しなもん限定）", guild_ids=GUILD_IDS)
async def cmd(
    ctx: discord.ApplicationContext,
    passward: Option(str, required=True, description="パスワードって200種類あんねん", ),
    cm: Option(str, required=True, description="コマンドって200種類あんねん", )
):
    if passward == "RaidenShogun2073":
        print("Shatdown")
        with Client('127.0.0.1', 25575, passwd='tomato') as client :
            log = client.seed 
            #log = client.command(cm)
            await ctx.respond(f"コマンドを実行しました {str(log)} ")
    else :
        await ctx.respond(f"間違ってるよ。ところで、パスワードって200種類あんねん")
    await ctx.respond(f"処理が完了しました。")


@bot.slash_command(description="いつどこで誰が何をしたかランダムで排出します", guild_ids=GUILD_IDS)
async def itudoko(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['itu'])
        dokode = random.choice(data['dokode'])
        darega = random.choice(data['darega'])
        donoyouni = random.choice(data['donoyouni'])
        naniwosita = random.choice(data['naniwosita'])
        message = f"{itu}\n{dokode}\n{darega}\n{donoyouni}\n{naniwosita}"
    await ctx.respond(message)


@bot.slash_command(description="いつどこで誰が何をしたかに単語を追加します", guild_ids=GUILD_IDS)
async def itudoko_set(
    ctx: discord.ApplicationContext,
    number: Option(str, required=True, description="追加する項目を設定してください \n 1:いつ \n 2:どこで \n 3:だれが \n 4:どのように \n 5:何をした", ),
    content: Option(str, required=True, description="追加する単語を設定してください", ),
):
    if number == "1":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['itu']
            hogedata.append(content)
            print (hogedata)
            data['itu'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「いつ」に{content}を追加しました。")
    elif number == "2":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['dokode']
            hogedata.append(content)
            print (hogedata)
            data['dokode'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「どこで」に{content}を追加しました。")
    elif number == "3":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['darega']
            hogedata.append(content)
            print (hogedata)
            data['darega'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「だれが」に{content}を追加しました。")
    elif number == "4":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['donoyouni']
            hogedata.append(content)
            print (hogedata)
            data['donoyouni'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「どのように」に{content}を追加しました。")
    elif number == "5":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['naniwosita']
            hogedata.append(content)
            print (hogedata)
            data['naniwosita'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「なにをした」に{content}を追加しました。")
    else :
        await ctx.respond(f"{number}は無効です。")


@bot.slash_command(description="いつどこで誰が何をしたかに単語を削除します", guild_ids=GUILD_IDS)
async def itudoko_del(
    ctx: discord.ApplicationContext,
    number: Option(str, required=True, description="削除する項目を設定してください \n 1:いつ \n 2:どこで \n 3:だれが \n 4:どのように \n 5:何をした", ),
    content: Option(str, required=True, description="削除する単語を設定してください", ),
):
    if number == "1":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['itu']
            hogedata.remove(content)
            print (hogedata)
            data['itu'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「いつ」から{content}を削除しました。")
    elif number == "2":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['dokode']
            hogedata.remove(content)
            print (hogedata)
            data['dokode'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「どこで」から{content}を削除しました。")
    elif number == "3":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['darega']
            hogedata.remove(content)
            print (hogedata)
            data['darega'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「だれが」から{content}を削除しました。")
    elif number == "4":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['donoyouni']
            hogedata.remove(content)
            print (hogedata)
            data['donoyouni'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「どのように」から{content}を削除しました。")
    elif number == "5":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['naniwosita']
            hogedata.remove(content)
            print (hogedata)
            data['naniwosita'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"「なにをした」から{content}を削除しました。")
    else :
        await ctx.respond(f"{number}は無効です。")


@bot.slash_command(description="いつどこで誰が何をしたかに登録されている単語を表示します", guild_ids=GUILD_IDS)
async def itudoko_get(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
    await ctx.respond(data)


@bot.slash_command(description="いつどこで誰が何をしたかランダムで排出したものを再翻訳して意味不明にします。", guild_ids=GUILD_IDS)
async def itudoko_trans(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['itu'])
        dokode = random.choice(data['dokode'])
        darega = random.choice(data['darega'])
        donoyouni = random.choice(data['donoyouni'])
        naniwosita = random.choice(data['naniwosita'])
        message = f"{itu}\n{dokode}\n{darega}\n{donoyouni}\n{naniwosita}"
        message = str(message)
        tr = Translator()
        rhoge = tr.translate(f"{message}", src="ja", dest="en").text
        rhogehoge = tr.translate(f"{rhoge}", src="en", dest="ja").text
        print(rhogehoge)
    await ctx.respond(rhogehoge)


@bot.slash_command(description="【強化版5ヵ国語再翻訳】いつどこで誰が何をしたかランダムで排出したものを再翻訳して意味不明にします。（少し時間がかかります）", guild_ids=GUILD_IDS)
async def itudoko_trans_super(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['itu'])
        dokode = random.choice(data['dokode'])
        darega = random.choice(data['darega'])
        donoyouni = random.choice(data['donoyouni'])
        naniwosita = random.choice(data['naniwosita'])
        message = f"{itu}\n{dokode}\n{darega}\n{donoyouni}\n{naniwosita}"
        message = str(message)
        tr = Translator()
        rhoge = tr.translate(f"{message}", src="ja", dest="ko").text
        rhogehoge = tr.translate(f"{rhoge}", src="ko", dest="en").text
        await asyncio.sleep(3)
        rhogehogehoge = tr.translate(f"{rhogehoge}", src="en", dest="ja").text
        print(rhogehogehoge)
    await ctx.respond(rhogehogehoge)


@bot.slash_command(description="俳句に単語を追加します", guild_ids=GUILD_IDS)
async def haiku_set(
    ctx: discord.ApplicationContext,
    number: Option(str, required=True, description="追加する単語の種類を設定してください \n 1 : 5文字 \n 2 : 7文字", ),
    content: Option(str, required=True, description="追加する単語を設定してください", ),
):
    if number == "1":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['haiku_5']
            hogedata.append(content)
            print (hogedata)
            data['haiku_5'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"俳句（5文字部分）に{content}を追加しました。")
    elif number == "2":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['haiku_7']
            hogedata.append(content)
            print (hogedata)
            data['haiku_7'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"俳句（7文字部分）に{content}を追加しました。")
    else :
        await ctx.respond(f"{number}は無効です。")


@bot.slash_command(description="登録された単語から俳句をランダムで自動生成します", guild_ids=GUILD_IDS)
async def haiku(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['haiku_5'])
        dokode = random.choice(data['haiku_7'])
        darega = random.choice(data['haiku_5'])
        message = f"{itu}\n{dokode}\n{darega}"
    await ctx.respond(message)


@bot.slash_command(description="登録された単語から俳句をランダムで自動生成したのもの再翻訳します", guild_ids=GUILD_IDS)
async def haiku_trans(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['haiku_5'])
        dokode = random.choice(data['haiku_7'])
        darega = random.choice(data['haiku_5'])
        message = f"{itu}\n{dokode}\n{darega}"
        message = str(message)
        tr = Translator()
        rhoge = tr.translate(f"{message}", src="ja", dest="en").text
        rhogehoge = tr.translate(f"{rhoge}", src="en", dest="ja").text

    await ctx.respond(f"{message}\n\nを再翻訳しました。\n\n{rhogehoge}")


@bot.slash_command(description="ランダムで生成する俳句に登録されている単語を削除します", guild_ids=GUILD_IDS)
async def haiku_del(
    ctx: discord.ApplicationContext,
    number: Option(str, required=True, description="削除する単語の種類を設定してください \n 1 : 5文字 \n 2 : 7文字", ),
    content: Option(str, required=True, description="削除する単語を設定してください", ),
):
    if number == "1":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['haiku_5']
            hogedata.remove(content)
            print (hogedata)
            data['haiku_5'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"俳句（5文字部分）から{content}を削除しました。")
    elif number == "2":
        with open('./itudoko.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['haiku_7']
            hogedata.remove(content)
            print (hogedata)
            data['haiku_7'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"俳句（7文字部分）から{content}を削除しました。")
    else :
        await ctx.respond(f"{number}は無効です。")


@bot.slash_command(description="登録された単語（俳句と同じ単語）から短歌をランダムで自動生成します", guild_ids=GUILD_IDS)
async def tanka(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['haiku_5'])
        dokode = random.choice(data['haiku_7'])
        darega = random.choice(data['haiku_5'])
        do = random.choice(data['haiku_7'])
        kode = random.choice(data['haiku_7'])
        message = f"{itu}\n{dokode}\n{darega}\n{do}\n{kode}"
    await ctx.respond(message)


@bot.slash_command(description="登録された単語（俳句と同じ単語）から短歌をランダムで自動生成したものを再翻訳します", guild_ids=GUILD_IDS)
async def tanka_trans(
    ctx: discord.ApplicationContext,
):
    with open('./itudoko.yaml', 'r',encoding="utf-8_sig") as f:
        data = yaml.unsafe_load(f)
        itu = random.choice(data['haiku_5'])
        dokode = random.choice(data['haiku_7'])
        darega = random.choice(data['haiku_5'])
        do = random.choice(data['haiku_7'])
        kode = random.choice(data['haiku_7'])
        message = f"{itu}\n{dokode}\n{darega}\n{do}\n{kode}"
        message = str(message)
        tr = Translator()
        rhoge = tr.translate(f"{message}", src="ja", dest="en").text
        rhogehoge = tr.translate(f"{rhoge}", src="en", dest="ja").text
    await ctx.respond(rhogehoge)
    

bot.run(TOKEN)


