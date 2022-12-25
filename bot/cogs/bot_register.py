import os
import random
import string
import asyncio
import discord
from captcha.image import ImageCaptcha
import discord
from discord.ext import commands
from discord.ui import *
from bot.database.mongo_normal import *
from bot.database.conn.mongo import MongoConnection

class bot_register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="봇을 사용할수 있도록 봇에 가입합니다.")
    async def 봇가입(self, ctx):
        await ctx.defer(ephemeral=True)
        regcheck = mongo_register(self.bot.mongo).register_check(ctx.author.id)
        if regcheck == True:
            register_embed_1 = discord.Embed(title="<a:no_stop_false:1056069138008768645>가입 실패", description="이미 가입되어 있습니다.", color=0xff0000)
            register_embed_1.set_footer(text="™Imagine💡")
            await ctx.respond(embed=register_embed_1)
        elif regcheck == False:
            letters = string.digits
            captcha = ''.join(random.choice(letters) for i in range(4))
            image = ImageCaptcha()
            image.generate(captcha)
            image.write(captcha, f'./cache/captcha/{captcha}.png')
            captchaFile = discord.File(f"./cache/captcha/{captcha}.png")
            await ctx.respond(content=f"캡차가 생성되었습니다. 15초 이내에 아래의 캡차를 입력해주세요.",file=captchaFile,ephemeral=True)
            #os.remove(f"./cache/captcha/{captcha}.png")
            def check(m: discord.Message):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                guess: discord.Message = await self.bot.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(title=f"**봇 가입**",color=0x4F84C4)
                timeout_embed.add_field(name=f"<a:no_stop_false:1056069138008768645>**캡차 입력시간 초과!**", value="명령어를 다시 실행하여 다시 시도해주세요", inline=True) 
                timeout_embed.set_footer(text="™Imagine💡")
                await ctx.respond(embed=timeout_embed, ephemeral=True) 
            else:
                if guess.content == captcha:
                    await guess.delete(delay=2)
                    class Button(discord.ui.View):
                        @discord.ui.button(label=f"동의", style=discord.ButtonStyle.green,emoji="✅")
                        async def agree(self, button: discord.ui.Button, interaction: discord.Interaction):
                            view = discord.ui.View()
                            view.add_item(discord.ui.Button(label='매니저 서버', url='https://git.tros.lol', row=0))
                            mongo_register(MongoConnection()).register(ctx.author.id)
                            register_embed_4 = discord.Embed(title="<a:emoji_2:1056059723083956254>가입 성공", description="봇 가입이 완료되었습니다.", color=0x00ff00)
                            register_embed_4.set_footer(text="™Imagine💡")
                            await interaction.response.edit_message(embed=register_embed_4, view=view)
                        @discord.ui.button(label=f"동의 안함", style=discord.ButtonStyle.red,emoji="❎")
                        async def disagree(self, button: discord.ui.Button, interaction: discord.Interaction):
                            view = discord.ui.View()
                            view.add_item(discord.ui.Button(label='매니저 서버', url='https://git.tros.lol', row=0))
                            register_embed_3 = discord.Embed(title="<a:no_stop_false:1056069138008768645>가입 실패", description="봇 가입이 취소되었습니다.", color=0x00ff00)
                            register_embed_3.set_footer(text="™Imagine💡")
                            await interaction.response.edit_message(embed=register_embed_3, view=view)
                    register_embed_2 = discord.Embed(title="봇 가입", description="봇 가입을 위해서는 아래의 버튼을 눌러 동의해주세요.", color=0x00ff00)                        
                    register_embed_2.set_footer(text="™Imagine💡")
                    await ctx.respond(embed=register_embed_2,view=Button(), ephemeral=True)
                else:
                    await guess.delete(delay=2)
                    embed2 = discord.Embed(title=f"**봇 가입**",color=0x4F84C4)
                    embed2.add_field(name=f"<a:no_stop_false:1056069138008768645>**캡차가 틀렸어요!**", value="명령어를 다시 실행하여 다시 시도해주세요.", inline=True) 
                    embed2.set_footer(text="™Imagine💡")
                    await ctx.respond(embed=embed2, ephemeral=True) 
def setup(bot):
    bot.add_cog(bot_register(bot))
