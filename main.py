import discord
import requests

TOKEN = 'GAMITIN MO NALANG TOKEN BOT MO'

def translate_text(text, target_lang='ja'):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"en|{target_lang}"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Debug information
    print(f"Request URL: {response.url}")
    print(f"Response Data: {data}")

    return data.get("responseData", {}).get("translatedText", "Translation error")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$translate'):
        text = message.content[len('$translate '):].strip()
        if not text:
            await message.channel.send('Usage: !translate <text>')
            return
        async with message.channel.typing():
            translation = translate_text(text)
        
        await message.channel.send(f'Translation: {translation}')
client.run(TOKEN)
