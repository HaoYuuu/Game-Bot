import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random


def printBoard(board):
    b = (f'{board[7]}{board[8]}{board[9]}\n{board[4]}{board[5]}{board[6]}\n{board[1]}{board[2]}{board[3]}')
    return b


def choosePlayerLetter(letter):
    if letter == "X":
        return [":regional_indicator_x:", ":regional_indicator_o:"]
    else:
        return [":regional_indicator_o:", ":regional_indicator_x:"]


def whoFirst(letter):
    if letter == ":regional_indicator_x:":
        return "player"
    else:
        return "computer"


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(b, l):
    return ((b[1] == l and b[2] == l and b[3] == l) or
            (b[4] == l and b[5] == l and b[6] == l) or
            (b[7] == l and b[8] == l and b[9] == l) or
            (b[1] == l and b[4] == l and b[7] == l) or
            (b[2] == l and b[5] == l and b[8] == l) or
            (b[3] == l and b[6] == l and b[9] == l) or
            (b[1] == l and b[5] == l and b[9] == l) or
            (b[3] == l and b[5] == l and b[7] == l))


def copyBoard(board):
    cboard = []
    for i in board:
        cboard.append(i)
    return cboard


def isSpaceEmpty(board, move):
    return board[move] == ":blue_square:"


def chooseRandomMove(board, moveList):
    possibleMove = []
    for i in moveList:
        if isSpaceEmpty(board, i):
            possibleMove.append(i)
    if len(possibleMove) != 0:
        return random.choice(possibleMove)
    else:
        return None


def getComputerMove(board, computerLetter):
    if computerLetter == ":regional_indicator_x:":
        playerLetter = ":regional_indicator_o:"
    else:
        playerLetter = ":regional_indicator_x:"
    for i in range(1, 10):
        copy = copyBoard(board)
        if isSpaceEmpty(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i
    for i in range(1, 10):
        copy = copyBoard(board)
        if isSpaceEmpty(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i
    return chooseRandomMove(board, list(range(1, 10)))


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceEmpty(board, i):
            return False
    return True


class Game2(Cog_Extension):

    @commands.command()
    async def g2(self, ctx):
        await ctx.send("**<< 圈圈叉叉 >>**\n```規則 : 率先連線者獲勝```")
        theNumberBoard = " ,:one:,:two:,:three:,:four:,:five:,:six:,:seven:,:eight:,:nine:".split(
            ",")
        round = 0

        while True:
            await ctx.send(printBoard(theNumberBoard))
            theBoard = [':blue_square:'] * 10
            letter = ''
            while not (letter == "O" or letter == "X"):
                await ctx.send("選擇O/X (X為先手) :")

                def check(msgs):
                    return msgs.author == ctx.author and msgs.channel == ctx.channel
                msgs = await self.bot.wait_for('message', check=check)
                msg = msgs.content
                letter = str(msg).upper()
            playerLetter, computerLetter = choosePlayerLetter(letter)
            turn = whoFirst(playerLetter)
            isPlaying = True
            await ctx.send("---------- START ----------")

            while isPlaying:
                if turn == "player":
                    move = ''
                    times = 0
                    while move not in "1 2 3 4 5 6 7 8 9".split(" ") or not isSpaceEmpty(theBoard, int(move)):
                        await ctx.send("選擇移動位置(1~9):")

                        def check(msgs):
                            return msgs.author == ctx.author and msgs.channel == ctx.channel
                        msgs = await self.bot.wait_for('message', check=check)
                        msg = msgs.content
                        move = str(msg)
                        times += 2
                    await ctx.channel.purge(limit=times)
                    makeMove(theBoard, playerLetter, int(move))
                    round += 1
                    if round > 1:
                        await ctx.channel.purge(limit=1)
                    if isWinner(theBoard, playerLetter):
                        await ctx.send(printBoard(theBoard))
                        await ctx.send("> :confetti_ball: **玩家獲勝** :confetti_ball:")
                        isPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            await ctx.send(printBoard(theBoard))
                            await ctx.send("> :scales: **平手** :scales:")
                            break
                        else:
                            await ctx.send(printBoard(theBoard))
                            turn = "computer"
                else:
                    move = getComputerMove(theBoard, computerLetter)
                    makeMove(theBoard, computerLetter, move)
                    round += 1
                    if round > 1:
                        await ctx.channel.purge(limit=1)
                    if isWinner(theBoard, computerLetter):
                        await ctx.send(printBoard(theBoard))
                        await ctx.send("> :wrench: **bot獲勝** :wrench:")
                        isPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            await ctx.send(printBoard(theBoard))
                            await ctx.send("> :scales: **平手** :scales:")
                            break
                        else:
                            await ctx.send(printBoard(theBoard))
                            turn = "player"
            await ctx.send("是否再玩一場?(yes/no)")

            def check(msgs):
                return msgs.author == ctx.author and msgs.channel == ctx.channel
            msgs = await self.bot.wait_for('message', check=check)
            msg = msgs.content
            if not str(msg).upper().startswith("Y"):
                await ctx.send("**感謝遊玩**:video_game:\n**期待下次相遇**:wave:")
                break

async def setup(bot):
    await bot.add_cog(Game2(bot))
