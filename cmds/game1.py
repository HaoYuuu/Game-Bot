import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import json

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


def inputGuess(guessList, message):
    for i in range(4):
        guessList[i] = message[i]
    return guessList


def countAB(answerList, guessList):
    A = B = 0
    for i in range(4):
        for j in range(4):
            if answerList[i] == guessList[i]:
                A += 1
                break
            elif answerList[i] == guessList[j]:
                B += 1
    return A, B


class Game1(Cog_Extension):

    @commands.command()
    async def g1(self, ctx):

        
        def check(msgs):
            return msgs.author == ctx.author and msgs.channel == ctx.channel
        

        list = "0 1 2 3 4 5 6 7 8 9".split(" ")
        answerList = []
        guessList = [0, 0, 0, 0]
        A = B = round = 0
        for i in range(4):
            answerList.append(list.pop(random.randint(0, 9-i)))
        await ctx.send(jdata["rule1"])
        isPlaying = True

        while isPlaying:
            while A < 4:
                A = B = 0
                round += 1
                await ctx.send(f'------- round {round} -------')

                while True:
                    await ctx.send("請輸入答案:")
                    msgs = await self.bot.wait_for('message', check=check)
                    message = msgs.content
                    await ctx.channel.purge(limit=1)
                    await ctx.send(msgs.content)
                    if message.isdigit():
                        if len(message) == 4:
                            if message.count(message[0]) == 1 and message.count(message[1]) == 1 \
                                    and message.count(message[2]) == 1:
                                break
                            else:
                                await ctx.send("(數字不能重複)")
                        else:
                            await ctx.send("(輸入四位數)")
                    else:
                        await ctx.send("(輸入數字)")

                A, B = countAB(answerList, inputGuess(guessList, message))
                await ctx.send(f'結果:{A}A{B}B')
            await ctx.send(f'> :confetti_ball: **恭喜答對** :confetti_ball:\
                \n> **答案為"{message}"**\n> **共花了{round}回合!**')
            await ctx.send("是否再玩一場?(yes/no)")
            msgs = await self.bot.wait_for('message', check=check)
            msg = msgs.content
            if not str(msg).upper().startswith("Y"):
                await ctx.send("**感謝遊玩**:video_game:\n**期待下次相遇**:wave:")
                break


async def setup(bot):
    await bot.add_cog(Game1(bot))
