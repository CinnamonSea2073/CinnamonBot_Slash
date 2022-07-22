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

load_dotenv()
TOKEN = "ODk0MTU2OTAxMDc4Njc1NDg2.GqIRwc.rFIww51BQZ_qt_Z3DkFGoeKjmRqAa79JX7GBdY"
bot = discord.Bot()
GUILD_IDS = [879288794560471050]  # ← BOTのいるサーバーのIDを入れます

@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


itudoko = SlashCommandGroup('itudoko', 'test') # これがグループ定義

@itudoko.command(name='trans', description='再翻訳で支離滅裂な文章に変換します') # グループ定義したcommandのデコレータを利用する
async def itudokotrans(self, ctx, loop: Option(int, description='再翻訳回数を上げて精度を低めます デフォルト loop=1', min_value=1, max_value=5, default=1, required=False)):
        word = f'{random.choice(ItudokoCog.stack[0])}{random.choice(ItudokoCog.stack[1])}{random.choice(ItudokoCog.stack[2])}{random.choice(ItudokoCog.stack[3])}'
        await ctx.respond(f'翻訳前 : {word}')
        dest_word = ItudokoCog.random_transe(
            word=word,
            lang='ja',
            loop=loop,
            lang_codes=copy(ItudokoCog.lang_codes)
        )
        await ctx.interaction.edit_original_message(content=f'翻訳前 : {word}\n翻訳後 : {dest_word}')


    # 値と表示名分離するのに配列定義すると見やすい
itudoko_list = [
    OptionChoice(name='いつ', value=0),
    OptionChoice(name='どこで', value=1),
    OptionChoice(name='だれが', value=2),
    OptionChoice(name='何をした', value=3)
    ]

@itudoko.command(name="set", description="いつどこワードを追加します") # グループ定義したcommandのデコレータを利用する
async def itudokoset(
                      self, 
                      ctx, 
                      choise: Option(int, choices=itudoko_list), # ここのchoicesの値にOptionChoiceの配列を持たせてやればOK
                      value: Option(str, description='リテラルを決定してね')):
        ItudokoCog.stack[choise].append(value)
        ItudokoCog.wright_json(stack=ItudokoCog.stack)
        await ctx.respond(f'{value}をセットしました', ephemeral=True)

@itudoko.command(name='get', description='今まで貯めた文字列でランダムにいつどこいます') # グループ定義したcommandのデコレータを利用する
async def itudokoget(self, ctx):
        await ctx.respond(
            f'{random.choice(ItudokoCog.stack[0])}{random.choice(ItudokoCog.stack[1])}{random.choice(ItudokoCog.stack[2])}{random.choice(ItudokoCog.stack[3])}')

bot.run(TOKEN)