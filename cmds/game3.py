import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random


class Game3(Cog_Extension):

    @commands.command()
    async def g3(self, ctx):
        await ctx.send("**<< 終極密碼(1~100) >>**\n```規則 : 由1到100猜測答案\n       範圍隨猜測漸漸縮小```")
        number = {1: ":one:", 2: ":two:", 3: ":three:", 4: ":four:", 5: ":five:",
                6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:", 0: ":zero:", 10: ":one::zero:", }
        isPlaying = True

        while isPlaying:
            answer = random.randint(1, 100)
            min, max = 1, 100
            guess = times = 0
            while guess != answer:
                times += 1
                while True:
                    await ctx.send(f'--------第{times}次猜測--------')

                    def check(msgs):
                        return msgs.author == ctx.author and msgs.channel == ctx.channel
                    msgs = await self.bot.wait_for('message', check=check)
                    guess = str(msgs.content)
                    if guess.isdigit():
                        guess = int(guess)
                        if not (guess < min or guess > max):
                            break
                        else:
                            await ctx.send("(數字不在範圍中)")
                    else:
                        await ctx.send("(請輸入數字)")
                await ctx.channel.purge(limit=1)
                await ctx.send(f'{number[guess//10]}{number[guess%10]}')
                if guess != answer:
                    if guess >= min and guess < answer:
                        min = guess + 1
                    if guess <= max and guess > answer:
                        max = guess - 1
                    await ctx.send(f'範圍 : {number[min//10]}{number[min%10]} ~ {number[max//10]}{number[max%10]}')
                else:
                    await ctx.send(f'> :confetti_ball: **猜中了** :confetti_ball:\n> **(共猜了{times}次)**')
            await ctx.send("是否再玩一場?(yes/no)")

            def check(msgs):
                return msgs.author == ctx.author and msgs.channel == ctx.channel
            msgs = await self.bot.wait_for('message', check=check)
            msg = msgs.content
            if not str(msg).upper().startswith("Y"):
                await ctx.send("**感謝遊玩**:video_game:\n**期待下次相遇**:wave:")
                break

async def setup(bot):
    await bot.add_cog(Game3(bot))
