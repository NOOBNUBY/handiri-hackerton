import discord
from discord.ext import commands
from discord.ui import *
from bot.config import *

class Normal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    class MyView(discord.ui.View):
        async def on_timeout(self):
            for child in self.children: #시간초과 설정
                child.disabled = True
            timeoutembed = discord.Embed(title="시간 초과",description="봇의 자원소모와 디스코드 API기술문제로 30초가 지나면 비활성화됩니다.",color=0x4F84C4)
            await self.message.edit(embed=timeoutembed, view=self)
        @discord.ui.select(
            placeholder = "명령어 목록", 
            options = [
                discord.SelectOption(label="📚 기본",value="1",description="봇의 기본 명령어를 표시합니다."),
                discord.SelectOption(label="🖼️ 업스케일링",value="2",description="봇의 업스케일링 기능에 관한 명령어를 표시합니다."),
                discord.SelectOption(label="🎨 AI그림생성",value="3",description="봇의 AI그림생성 관련 기능에 관한 명령어를 표시합니다."),
                discord.SelectOption(label="🤖 사진 분석",value="4",description="봇의 사진 분석 기능에 관한 기능에 관한 명령어를 표시합니다.") 
            ]
        ) 
        async def select_callback(self, select, interaction):
            select.disabled = True
            if select.values[0] == "1":
                embed1= discord.Embed(title=f"📚 기본", description=f"봇의 기본 명령어를 확인합니다.", color=0x1DF289)
                embed1.add_field(name="</도움말:13>",value=f"기본 명령어를 확인합니다.",inline=False)
                embed1.add_field(name="/봇가입",value=f"봇의 서비스를 사용하기 위해 가입할수 있는 명령어입니다.",inline=False)
                embed1.add_field(name="/봇정보",value=f"봇의 정보를 확인할수 있는 명령어입니다.",inline=False)
                embed1.add_field(name="/ping",value=f"봇의 ping상태를 확인할 수 있는 명령어입니다.",inline=False)
                embed1.set_footer(text="™Imagine💡")
                await interaction.response.edit_message(embed=embed1)
            if select.values[0] == "2":
                embed2 = discord.Embed(title=f"🖼️ 업스케일링", description=f"봇의 업스케일링 기능에 대한 명령어를 표시합니다.", color=0x0455D8)
                embed2.add_field(name="/업스케일",value=f"이미지를 업스케일링합니다.",inline=False)
                embed2.add_field(name="/업스케일 내역",value=f"자신이 이미지를 업스케일링한 목록을 확인합니다.",inline=False)
                embed2.set_footer(text="™Imagine💡")
                await interaction.response.edit_message(embed=embed2)
            if select.values[0] == "3":
                embed3 = discord.Embed(title=f"🎨 AI그림생성", description=f"봇의 AI그림생성 관련 기능에 대한 명령어를 표시합니다.", color=0xf44336)
                embed3.add_field(name="/AI그림생성",value=f"AI가 그림을 생성합니다.",inline=False)
                embed3.set_footer(text="™Imagine💡")
                await interaction.response.edit_message(embed=embed3)
            if select.values[0] == "4":
                embed4 = discord.Embed(title=f"🤖 사진분석", description=f"봇의 사진 분석 기능에 대한 명령어를 표시합니다.", color=0xBFEAF5)
                embed4.add_field(name="/사진분석",value=f"사진을 분석합니다.",inline=False)
                embed4.set_footer(text="™Imagine💡")
                await interaction.response.edit_message(embed=embed4)
    @discord.slash_command(description="봇 명령어와 사용법을 나열합니다.")
    async def 도움말(self, ctx):
        helppembed = discord.Embed(title=f"📃 명령어", description=f"명령어를 확인합니다.", color=0x4F84C4)
        helppembed.set_footer(text="™Imagine💡")
        await ctx.respond(embed=helppembed,view=self.MyView(timeout=30))

    @discord.slash_command(description="봇 정보를 표시합니다.")
    async def 봇정보(self, ctx):
        embed5 = discord.Embed(title=f"🤖 봇 정보",description=f"Imagine봇의 정보",color=0x01BAEF)
        embed5.add_field(name="**봇 소개**",value=f"Imagine 봇은 사진 업스케일링, AI그림생성,사진분석의 기능들이 있습니다.\n주요 기능으로는 업스케일링이 있습니다.",inline=False)
        embed5.add_field(name="**💻 개발자**",value=f"<@587082914899034113>\n<@878092667156856882>",inline=False)
        embed5.set_footer(text="™Imagine💡")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='invite link',style=discord.ButtonStyle.link, url='https://tmddn3070.live'))
        await ctx.respond(embed=embed5,view=view)

    @discord.slash_command(description="봇의 상태를 확인할 수 있는 명령어입니다.")
    async def 핑(self, ctx):
        if round(self.bot.latency * 1000) <= 180:
            embed=discord.Embed(title="퐁!",description=f":ping_pong: \n 현재 게이트웨이 지연시간 : **{round(self.bot.latency *1000)} ms **", color=0x44ff44)
            embed.set_footer(text="™Imagine💡")
        elif round(self.bot.latency * 1000) <= 190:
            embed=discord.Embed(title="퐁!",description=f":ping_pong: \n 현재 게이트웨이 지연시간 : **{round(self.bot.latency *1000)} ms **", color=0xffd000)
            embed.set_footer(text="™Imagine💡")
        elif round(self.bot.latency * 1000) <= 200:
            embed=discord.Embed(title="퐁!",description=f":ping_pong: \n 현재 게이트웨이 지연시간 : **{round(self.bot.latency *1000)} ms **", color=0xff6600)
            embed.set_footer(text="™Imagine💡")
        else:
            embed=discord.Embed(title="퐁!",description=f":ping_pong: \n 현재 게이트웨이 지연시간 : **{round(self.bot.latency *1000)} ms **", color=0x990000)
            embed.set_footer(text="™Imagine💡")
        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(Normal(bot))