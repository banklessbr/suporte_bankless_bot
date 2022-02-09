import os
import json
import discord

from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

class FaqButton(Button):
    def __init__(self, label, message):
        self.message = message
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction):
        print('Interaction Received')
        try:
            await interaction.response.send_message(self.message, ephemeral=True)
        except Exception as e:
            print(e)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD_NAME)
    print(f'Connected {bot.user} to {guild}')

    await bot.wait_until_ready()
    print('Bot ready on background task')

    guild = discord.utils.get(bot.guilds, name=GUILD_NAME)
    channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

    with open('buttons.json') as fp:
        data = json.load(fp)

    view = View(timeout=False)
    for button in data:
        view.add_item(FaqButton(label=button, message=data[button]))

    
    with open('mensagem.json') as fp:
        bodyMessage = json.load(fp)

    await channel.send(bodyMessage, view=view)
    # await channel.send(f'Bem-vindo ao Canal do Discord do Bankless Brasil! Veja nosso FAQ:', view=view)
    print('Message sent')


bot.run(DISCORD_TOKEN)
