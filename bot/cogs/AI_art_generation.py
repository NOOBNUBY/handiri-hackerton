import os
import asyncio
import httpx
import random
import string
import base64 
import discord
from discord.commands import Option
from discord.ext import commands
from discord.ui import *
from bot.config import *
from bot.database.mongo_logging import *
from bot.database.mongo_normal import *
class aiart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @discord.slash_command(description="AI그림을 생성합니다.")
    async def ai그림생성(self, ctx, 프롬포트: Option(str, "AI그림을 생성할때 사용할 프롬포트를 입력합니다(영문)", required = False, default = None), 부정프롬포트: Option(str, "AI그림을 생성할때 사용할 네거티브 프롬포트를 입력합니다(영문)", required = False, default = None), 개인모드: Option(bool, "개인모드를 활성화한다면 생성된 그림이 나에게만 보입니다", required = True, default = False), 해상도: Option(str, "생성할 그림의 해상도를 설정합니다", choices=["512x512", "512x768"], required = True, default = "512x768"), 프롬포트표시: Option(bool, "프롬포트를 표시할지 말지를 설정합니다", required = True, default = True)):
        register_check = mongo_register(self.bot.mongo).register_check(ctx.author.id)
        if register_check == False:
            await ctx.respond(embed=discord.Embed(title="<a:no_stop_false:1056069138008768645> 봇에 가입이 필요합니다.",description="AI그림생성 기능을 사용하기 위해서는 봇에 가입이 필요합니다.",color=0xff0000))
        else:
            prompt = str(프롬포트)
            negative_prompt = str(부정프롬포트)
            resolution = str(해상도)
            show_prompt = bool(프롬포트표시)
            mongo_logging(self.bot.mongo).insert_log(ctx.author.id,0)
            if 프롬포트 == "None" or None:
                prompt = "best_quality,masterpiece"
            if 부정프롬포트 == "None" or None:
                negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"  
            private_mode = 개인모드
            if ctx.channel.is_nsfw() == False:
                negative_prompt = negative_prompt + ", nsfw"
            imgid = ''.join(random.choice(string.digits) for i in range(35))
            url = ""
            embed = discord.Embed(title="<a:emoji_3:1056060444823015444>생성중",description="<a:emoji_2:1056059723083956254>성공적으로 생성 대기열에 추가됬어요!\n트래픽과 대기열 상태에 따라 생성이 오래걸릴수도 있어요.",color=0xEDDEA4)
            embed.set_footer(text="™Imagine💡")
            notify = await ctx.send(embed=embed,delete_after=6)
            await ctx.defer(ephemeral=private_mode)
            if resolution == "512x512":
                garo = 512
            elif resolution == "512x768":
                garo = 768
            else:
                garo = 768
            try:
                payload = {
                "prompt": prompt,
                "sampler_name": "DPM++ 2M Karras",
                "negative_prompt": negative_prompt,
                "batch_size": 1,
                "steps": 32,
                "cfg_scale": 12,
                "width": 512,
                "height": garo
                }
                async with httpx.AsyncClient() as client:
                    result = await client.post(url, json=payload, timeout=None)
                result = result.json()
                with open(f"./cache/aiart/{imgid}.png", "wb") as fh:
                    fh.write(base64.b64decode(result["images"][0]))
                """send image"""
                file = discord.File(f"./cache/aiart/{imgid}.png")
                embed = discord.Embed(title="<a:emoji_2:1056059723083956254>생성완료",description="생성이 완료되었습니다.",color=0xEDDEA4)
                if show_prompt == True:
                    embed.add_field(name="프롬포트", value=prompt, inline=False)
                    embed.add_field(name="부정프롬포트", value=negative_prompt, inline=False)
                else:
                    pass
                embed.set_image(url=f"attachment://{imgid}.png")
                embed.set_footer(text="™Imagine💡")
                await ctx.respond(embed=embed, file=file, ephemeral=private_mode)
            except Exception as e:
                raise Exception(e)
         #   error_embed = discord.Embed(title="<a:no_stop_false:1056069138008768645>그림 생성에 실패했습니다", description="그림 생성에 실패했습니다. 나중에 다시시도해주세요.", color=0xff0000)
         #   await ctx.respond(embed=error_embed, ephemeral=private_mode)
        #os.remove(f"./cache/aiart/{imgid}.png")


def setup(bot):
    bot.add_cog(aiart(bot))