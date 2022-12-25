import httpx
import discord
import asyncio
from discord.ext import commands
from discord.ui import *
from bot.config import *
from bot.database.mongo_logging import *
from bot.database.mongo_normal import *
class Picture_analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="사진을 분석합니다.")
    async def 사진분석(self,ctx):
        register_check = mongo_register(self.bot.mongo).register_check(ctx.author.id)
        if register_check == False:
            await ctx.respond(embed=discord.Embed(title="<a:no_stop_false:1056069138008768645> 봇에 가입이 필요합니다.",description="이미지 분석기능을 이용하기 위해서는 봇에 가입이 필요합니다.",color=0xff0000))
        else:
            mongo_logging(self.bot.mongo).insert_log(ctx.author.id,2)
            embed = discord.Embed(title="<a:emoji_1:1056059699667140678> 원하시는 사진을 보내주세요!",description="60초 안에 원하는 사진을 디스코드 채팅창에 드래그 드랍!",color=0xC1B4AE)
            embed.set_footer(text="™Imagine💡")
            await ctx.respond(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(title="⏰ 시간 초과",description="봇의 리소스 관리를 위해 60초 안에 사진을 보내야해요!",color=0xff0000)
                timeout_embed.set_footer(text="™Imagine💡")
                await ctx.send(embed=timeout_embed)
            else:
                if msg.attachments:
                    url = msg.attachments[0].url
                    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".webp"):
                        try:
                            """using httpx"""
                            async with httpx.AsyncClient() as client:
                                r = await client.post(f"https://deepdanbooru.donmai.us/?url={url}&min_score=0.35")
                                r = r.json()
                            embed1 = discord.Embed(title="<a:emoji_3:1056060444823015444>분석중",description="분석중입니다 조금만 기다려주세요.",color=0xddf2d7)
                            embed1.set_footer(text="™Imagine💡")
                            original_m = await ctx.respond(embed=embed1)
                            for i in range(0,15):
                                r[i][1] = round(r[i][1]*100,2)
                            embed = discord.Embed(title="💻 분석 결과",description=f"🖼️ 분석한 사진: {url}",color=0xEAF2D7)
                            embed.set_thumbnail(url=url)
                            embed.add_field(name=f"📑일치도",value="".join(f"**{r[i][0]}**: **{r[i][1]}**%\n" for i in range(0,15)),inline=True) 
                            embed.add_field(name=f"📑TAG",value="".join(f"**{r[i][0]}**," for i in range(0,15)),inline=True)
                            embed.set_footer(text="™Imagine💡")                       
                            await original_m.edit(embed=embed)
                        except Exception as e:
                            print(e)
                            error=discord.Embed(title="<a:no_stop_false:1056069138008768645>ERROR",description="분석 중 오류가 발생했어요!\n<@587082914899034113> <@878092667156856882>한테\n문의 해주세요.",color=0xff0000)
                            error.set_footer(text="™Imagine💡")
                            await ctx.respond(embed=error,ephemeral=True)
                    else:
                        file_not_supported_embed = discord.Embed(title="<a:no_stop_false:1056069138008768645>지원하지 않는 확장자에요!",description="지원하는 확장자는 png, jpg, jpeg, webp에요",color=0xff0000)
                        file_not_supported_embed.set_footer(text="™Imagine💡")
                        await ctx.send(embed=file_not_supported_embed)
                else:
                    file_not_found_embed = discord.Embed(title="<a:no_stop_false:1056069138008768645>첨부된 파일이 없어요!",description="제대로된 이미지가 맞거나 파일이 첨부되어있는지 확인해주세요!",color=0xff0000)
                    file_not_found_embed.set_footer(text="™Imagine💡")
                    await ctx.send(embed=file_not_found_embed)


def setup(bot):
    bot.add_cog(Picture_analyze(bot))