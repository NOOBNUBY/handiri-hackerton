import os
import string
import random
import asyncio
import httpx
import requests
import discord
import cloudinary
import cloudinary.uploader
from PIL import Image
from waifu2x_ncnn_vulkan_python import Waifu2x
from discord.ext import commands
from discord.ui import *
from bot.config import *
from bot.database.mongo_logging import *
from bot.database.mongo_normal import *


class upscale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="이미지를 업스케일링합니다.")
    async def 업스케일링(self, ctx):
        register_check = mongo_register(self.bot.mongo).register_check(ctx.author.id)
        if register_check == False:
            await ctx.respond(embed=discord.Embed(title="<a:no_stop_false:1056069138008768645> 봇에 가입이 필요합니다.",description="이미지 업스케일링을 하기 위해서는 봇에 가입이 필요합니다.",color=0xff0000))
        else:
            mongo_logging(self.bot.mongo).insert_log(ctx.author.id,1)
            embed = discord.Embed(title="<a:emoji_1:1056059699667140678> 원하시는 사진을 보내주세요!",description="60초 안에 원하는 사진을 디스코드 채팅창에 드래그 드랍!",color=0xC1B4AE)
            embed.set_footer(text="™Imagine💡")
            mse = await ctx.respond(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(title="⏰ 시간 초과",description="봇의 리소스 관리를 위해 60초 안에 사진을 보내야해요!",color=0xff0000)
                timeout_embed.set_footer(text="™Imagine💡")
                await ctx.send(embed=timeout_embed)
            else:
                imgid = ''.join(random.choice(string.digits) for i in range(35))
                if msg.attachments:
                    url = msg.attachments[0].url
                    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".webp"):
                        try:
                            input_img = Image.open(requests.get(url, stream=True).raw)
                            input_img.save(f"./cache/upscale/{imgid}.png")
                            waifu2x = Waifu2x(gpuid=0, scale=2, noise=3)
                            before_convert_image = Image.open(f"./cache/upscale/{imgid}.png")
                            out_image = waifu2x.process(before_convert_image)
                            out_image.save(f"./cache/upscale/{imgid}_upscaled.png")
                            """upload to cloudinary"""
                            cloudinary.uploader.upload(f"./cache/upscale/{imgid}_upscaled.png", public_id=imgid)
                            srcURL = cloudinary.CloudinaryImage(imgid).build_url()
                            """send to discord"""
                            embed1 = discord.Embed(title="<a:emoji_3:1056060444823015444>업스케일링중",description="업스케일링중입니다 조금만 기다려주세요.",color=0xddf2d7)
                            embed1.set_footer(text="™Imagine💡")
                            original_m = await ctx.respond(embed=embed1)
                            embed = discord.Embed(title="<a:emoji_2:1056059723083956254>업스케일링 완료",description=f"이미지 업스케일링이 완료되었습니다\n아래의 링크로 들어가 다운받아주세요.\n[이미지 링크]({srcURL})",color=0xD6C9C9)
                            embed.set_thumbnail(url=srcURL)
                            embed.set_footer(text="™Imagine💡")
                            await original_m.edit(embed=embed)
                            #await ctx.send(file=discord.File(f"./cache/upscale/{imgid}_upscaled.png"))
                            os.remove(f"./cache/upscale/{imgid}.png")
                            os.remove(f"./cache/upscale/{imgid}_upscaled.png")
                        except Exception as e:
                            raise Exception(e)
                    else:
                        error_embed = discord.Embed(title="<a:no_stop_false:1056069138008768645>오류 발생",description="이미지 파일이 아닙니다!",color=0xff0000)
                        error_embed.set_footer(text="™Imagine💡")
                        await ctx.send(embed=error_embed)
                else:
                    error_embed = discord.Embed(title="<a:no_stop_false:1056069138008768645>오류 발생",description="이미지 파일이 아닙니다!",color=0xff0000)
                    error_embed.set_footer(text="™Imagine💡")
                    await ctx.send(embed=error_embed)
                
    @discord.slash_command(description="업스케일링 내역을 확인합니다.")
    async def 업스케일링내역(self, ctx):
        register_check = mongo_register(self.bot.mongo).register_check(ctx.author.id)
        if register_check == False:
            await ctx.respond(embed=discord.Embed(title="<a:no_stop_false:1056069138008768645> 봇에 가입이 필요합니다.",description="이미지 업스케일링 내역을 확인하기 위해서는 봇에 가입이 필요합니다.",color=0xff0000))
        else:
            logs = mongo_logging(self.bot.mongo).get_logs(ctx.author.id,1)
            embeds = discord.Embed(title="<a:emoji_2:1056059723083956254>업스케일링 내역",description="업스케일링 내역은 10개만 표시합니다.",color=0x7C99B4)
            count = 0
            for i in logs:
                count = count + 1
                embeds.add_field(name=count,value=f"사용 시각:{i['time']}",inline=False)
            embeds.set_footer(text="™Imagine💡")
            await ctx.respond(embed=embeds)
def setup(bot):
    bot.add_cog(upscale(bot))
