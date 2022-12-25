import os
import discord
#import uvloop
from discord.ext import commands
import asyncio
from bot.config import *
from bot.database.conn.mongo import MongoConnection
cogs = []

intents=discord.Intents.all()

bot = commands.Bot(command_prefix="!@",intents=intents)#슬래시 커맨드의 사용으로 prefix는 필요 없음, debug_guilds는 슬커 테스트용

for filename in os.listdir('./bot/cogs'):
    if filename.endswith('.py'):
        cogs.append(filename)
        #print(filename[:-3])
        bot.load_extension(f'bot.cogs.{filename[:-3]}')
    if filename == '__pycache__':pass

#help명령어 삭제(보안용)
bot.remove_command("help")
#DB 함수 설정
bot.mongo = MongoConnection()

@bot.event
async def on_ready():
    print(f'봇:{bot.user} (ID: {bot.user.id})')
    print(f'{len(bot.guilds)}개 길드')
    print(f'파이코드 버전:{discord.__version__}')

print(f'cog {len(cogs)}개 로딩 완료')
bot.run(config['tokin'])
