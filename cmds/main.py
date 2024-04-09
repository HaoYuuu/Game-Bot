import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import datetime

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

class Main(Cog_Extension):

    @commands.command()
    async def helps(self, ctx):
        embed = discord.Embed(title="Discord Game Bot",
                            description="produced by HaoYu",
                            timestamp=datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))))
        embed.set_author(
            name="Game bot", icon_url=jdata['pic'])
        embed.set_thumbnail(
            url=jdata['pic'])
        embed.add_field(name=":gear:指令說明", value="> 指令前墜:「.」", inline=True)
        embed.add_field(name=":pushpin:指令列表(此指令)",
                        value="> ( 指令 : helps )", inline=True)
        embed.add_field(name="Game:one: < 1A2B >",
                        value="( 指令 : g1 )", inline=False)
        embed.add_field(name="Game:two: < 圈圈叉叉 >",
                        value="( 指令 : g2 )", inline=False)
        embed.add_field(name="Game:three: < 終極密碼 >",
                        value="( 指令 : g3 )", inline=False)
        embed.add_field(name="Game:four: < 猜拳 >",
                        value="( 指令 : g4 )", inline=False)
        embed.set_footer(text="Have a good time !")
        await ctx.send(embed=embed)
   
        
async def setup(bot):
    await bot.add_cog(Main(bot))
