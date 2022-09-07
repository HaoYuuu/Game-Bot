import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    print(">> Bot is online <<")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1016736903023829043)
    await channel.send(f'{member} join!')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1016736930316169276)
    await channel.send(f'{member} leave!')

bot.run('MTAxNjcxNTExODQxNzAyMzAxNw.GVb_9Z.GL0q9iwpETsYTbsE6z_jJmIN4-C94WYSRD1emo')
