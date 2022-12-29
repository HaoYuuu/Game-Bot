import discord
import json
import random
import datetime
import time
from discord.ext import commands

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    print(">> Bot is online <<")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata['Welcome_channel']))
    await channel.send(f'{member} join!')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata['Leave_channel']))
    await channel.send(f'{member} leave!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')


@bot.command()
async def pic(ctx):
    pic = discord.File(jdata['pic'])
    await ctx.send(file=pic)


@bot.command()
async def helps(ctx):
    embed = discord.Embed(title="Discord Game Bot",
                          description="producted by HaoYu",
                          timestamp=datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))))
    embed.set_author(
        name="Game bot", icon_url=jdata['pic_link'])
    embed.set_thumbnail(
        url=jdata['pic_link'])
    embed.add_field(name="Game1 < 1A2B >", value="( 指令 : g1 )", inline=False)
    embed.add_field(name="Game2 < 圈圈叉叉 >", value="( 指令 : g2 )", inline=False)
    embed.set_footer(text="Have a good time !")
    await ctx.send(embed=embed)


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


@bot.command()
async def g1(ctx):
    list = "0 1 2 3 4 5 6 7 8 9".split(" ")
    answerList = []
    guessList = [0, 0, 0, 0]
    A = B = round = 0
    for i in range(4):
        answerList.append(list.pop(random.randint(0, 9-i)))
    await ctx.send("<< 1A2B遊戲 >>")
    isPlaying = True
    while isPlaying:
        while A < 4:
            A = B = 0
            round += 1
            await ctx.send(f'------- round {round} -------')

            while True:
                await ctx.send("請輸入答案:")

                def check(msgs):
                    return msgs.author == ctx.author and msgs.channel == ctx.channel
                msgs = await bot.wait_for('message', check=check)
                message = msgs.content
                await ctx.channel.purge(limit=1)
                await ctx.send(msgs.content)
                if message.isdigit():
                    if len(message) == 4:
                        if message.count(message[0]) == 1 and message.count(message[1]) == 1 and message.count(message[2]) == 1:
                            break
                        else:
                            await ctx.send("(數字不能重複)")
                    else:
                        await ctx.send("(輸入四位數)")
                else:
                    await ctx.send("(輸入數字)")

            A, B = countAB(answerList, inputGuess(guessList, message))
            await ctx.send(f'結果:{A}A{B}B')
        await ctx.send(f':confetti_ball: 恭喜答對 :confetti_ball:\n答案為"{message}"\n共花了{round}回合!')
        await ctx.send("是否再玩一場?(yes/no)")

        def check(msgs):
            return msgs.author == ctx.author and msgs.channel == ctx.channel
        msgs = await bot.wait_for('message', check=check)
        msg = msgs.content
        if not str(msg).upper().startswith("Y"):
            break


@bot.command()
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)


@bot.command()
async def clean(ctx):
    await ctx.channel.purge(limit=1)


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


@bot.command()
async def g2(ctx):
    await ctx.send("<< 圈圈叉叉 >>")
    theNumberBoard = " ,:one:,:two:,:three:,:four:,:five:,:six:,:seven:,:eight:,:nine:".split(
        ",")
    round = 0
    await ctx.send(printBoard(theNumberBoard))
    while True:
        theBoard = [':blue_square:'] * 10
        letter = ''
        while not (letter == "O" or letter == "X"):
            await ctx.send("選擇O/X (X為先手) :")

            def check(msgs):
                return msgs.author == ctx.author and msgs.channel == ctx.channel
            msgs = await bot.wait_for('message', check=check)
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
                    msgs = await bot.wait_for('message', check=check)
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
                    await ctx.send(":confetti_ball: 玩家獲勝 :confetti_ball:")
                    isPlaying = False
                else:
                    if isBoardFull(theBoard):
                        await ctx.send(printBoard(theBoard))
                        await ctx.send(":scales: 平手 :scales:")
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
                    await ctx.send(":wrench: bot獲勝 :wrench:")
                    isPlaying = False
                else:
                    if isBoardFull(theBoard):
                        await ctx.send(printBoard(theBoard))
                        await ctx.send(":scales: 平手 :scales:")
                        break
                    else:
                        await ctx.send(printBoard(theBoard))
                        turn = "player"
        await ctx.send("是否再玩一場?(yes/no)")

        def check(msgs):
            return msgs.author == ctx.author and msgs.channel == ctx.channel
        msgs = await bot.wait_for('message', check=check)
        msg = msgs.content
        if not str(msg).upper().startswith("Y"):
            break


@bot.command()
async def a(ctx):
    await ctx.send(":seven::eight::nine:\n:four::five::six:\n:one::two::three:")
    time.sleep(1)
    await ctx.channel.purge(limit=1)
    await ctx.send(":blue_square::blue_square::blue_square:\n"*3)


@bot.command()
async def aa(ctx):
    await ctx.send(f"y or n")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("You said yes!")
    else:
        await ctx.send("You said no!")

bot.run(jdata['TAKEN'])
