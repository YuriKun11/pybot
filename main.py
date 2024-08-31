#HYUN'S PYTHON BOT
import discord
import requests
import json
from io import BytesIO
from discord.ext import commands
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.all())

YOUR_USER_ID = ILAGAY MO DITO YUNG USER_ID NG DISCORD MO

bot = commands.Bot(command_prefix='$', intents=discord.Intents.default())


async def get_anime(name):
  search_url = f"https://api.jikan.moe/v4/anime?q={name}&limit=1"

  response = requests.get(search_url)
  json_data = response.json()

  try:
    anime_list = json_data['data']
    if anime_list:
      first_anime = anime_list[0]
      title = first_anime['title']
      synopsis = first_anime['synopsis']
      image_url = first_anime['images']['jpg']['large_image_url']

      modified_synopsis = synopsis.replace("[Written by MAL Rewrite]",
                                           "[Hyun's Recommendation]").strip()

      kyot = f"**Sauce: {title}**\n{modified_synopsis}"

      image_response = requests.get(image_url)
      image = BytesIO(image_response.content)

      return kyot, image
    else:
      return "No anime data available.", None
  except KeyError as e:
    print(f"KeyError: {e}")
    return "Error fetching anime data.", None


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.author.id != YOUR_USER_ID:
    await message.channel.send("Sorry, you are not the owner of this bot")
    return

  if message.content.startswith('$help'):
    help_message = (
        "**Here are the available commands:**\n"
        "`$help` - Displays this help message.\n"
        "`$anime [name]` - Fetches anime information from Jikan API.")
    await message.channel.send(help_message)

  #CUSTOM COMMANDS
  elif message.content.startswith('$play paper frog'):
    await message.channel.send(
        'https://youtu.be/7-rRPJnilzs?si=MhdH5N1leqe3WrnE')

  elif message.content.startswith('$play gentle breeze'):
    await message.channel.send(
        'https://youtu.be/1TUnMwjLR_M?si=vd0kGNoqDvCCKSp6')

  elif message.content.startswith('$play tender is the night'):
    await message.channel.send(
        'https://youtu.be/W0OxaoTxmjY?si=7292QTeDtNFsXt4f')

  elif message.content.startswith('$anime '):
    anime_name = message.content[len('$anime '):]
    description, image = await get_anime(anime_name)

    if image:
      embed = discord.Embed(description=description)
      embed.set_image(url="attachment://anime_image.jpg")
      await message.channel.send(embed=embed,
                                 file=discord.File(image, 'anime_image.jpg'))
    else:
      await message.channel.send(description)


keep_alive()
client.run(
    'ILAGAY MO DITO YUNG TOKEN NG DISCORD BOT MO')
