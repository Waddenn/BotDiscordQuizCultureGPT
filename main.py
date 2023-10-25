import discord
from discord.ext import commands
import json
import openai
from app.utils.management_utils import clear
from app.utils.quiz_utils import quiz

with open("./config/config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config["TOKEN"]
API_KEY = config["API_KEY"]

openai.api_key = API_KEY

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} est connecté au serveur")


bot.add_command(clear)
bot.add_command(quiz)


bot.run(TOKEN)
