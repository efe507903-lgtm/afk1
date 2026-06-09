import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot hazır: {bot.user}")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ Önce bir ses kanalına gir!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect(self_deaf=True, self_mute=True)
    await ctx.send(f"🔇 **{channel.name}** kanalına sessiz bağlandım.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("❌ Zaten bir ses kanalında değilim.")
        return
    await ctx.voice_client.disconnect()
    await ctx.send("👋 Ses kanalından ayrıldım.")

@bot.command(name="afk")
async def afk(ctx, dakika: int = 0):
    if ctx.author.voice is None:
        await ctx.send("❌ Önce bir ses kanalına gir!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect(self_deaf=True, self_mute=True)
    if dakika > 0:
        await ctx.send(f"🔇 **{channel.name}** kanalında {dakika} dakika AFK modunda bekleyeceğim.")
        await asyncio.sleep(dakika * 60)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send(f"⏰ {dakika} dakika doldu, kanaldan ayrıldım.")
    else:
        await ctx.send(f"🔇 **{channel.name}** kanalında süresiz AFK modunda bekliyorum. (`!leave` ile çıkarabilirsin)")

bot.run(os.environ["TOKEN"])
