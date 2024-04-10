import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Game4(Cog_Extension):

    @commands.command()
    async def g4(self, ctx):


        def check(msgs):
            return msgs.author == ctx.author and msgs.channel == ctx.channel
        

        await ctx.send(jdata["rule4"])
        dict = {-1: ":v:", 0: ":fist:", 1: ":raised_hand:"}
        isPlaying = True

        while isPlaying:
            times = win = lose = 0
            while win < 2 and lose < 2:
                while True:
                    await ctx.send("請出拳:")
                    msgs = await self.bot.wait_for('message', check=check)
                    player = str(msgs.content)
                    if player.isdigit():
                        player = int(player)-2
                        if player in [-1, 0, 1]:
                            break
                        else:
                            await ctx.send("(輸入1~3)")
                    else:
                        await ctx.send("(輸入1~3)")

                computer = random.randint(-1, 1)
                await ctx.channel.purge(limit=2)
                await ctx.send(f'請出拳:{dict[player]}')

                await ctx.send(f'第{times+1}場結果:{dict[player]} vs. {dict[computer]}')

                if (player - computer == 1) or (player - computer == -2):
                    await ctx.send("(玩家獲勝:confetti_ball:)")
                    win += 1
                if (player - computer == -1) or (player - computer == 2):
                    await ctx.send("(電腦獲勝:wrench:)")
                    lose += 1
                if (player - computer == 0):
                    await ctx.send("(平手:scales:)")
                await ctx.send(f'----- <目前比數> {win}:{lose} -----')
                times += 1
            if win > lose:
                await ctx.send("> **最終結果 : 玩家獲勝!!!**")
            else:
                await ctx.send("> **最終結果 : 電腦獲勝!!!**")
            await ctx.send("是否再玩一場?(yes/no)")
            msgs = await self.bot.wait_for('message', check=check)
            msg = msgs.content
            if not str(msg).upper().startswith("Y"):
                await ctx.send("**感謝遊玩**:video_game:\n**期待下次相遇**:wave:")
                break


async def setup(bot):
    await bot.add_cog(Game4(bot))
