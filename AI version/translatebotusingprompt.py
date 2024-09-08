import discord
import subprocess
import asyncio

TOKEN = 'PALITAN MO NG DISCORD TOKEN MO'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # DEBUG NAKIKITA KO LAHAT NG MESSAGES
    print(f"Received message: '{message.content}' in channel: {message.channel}")

    if message.author == client.user:
        return

    if message.content.startswith('$AI '):
        prompt = message.content[len('$AI '):].strip()
        if not prompt:
            await message.channel.send("No prompt provided after `$AI`.")
            return
        
        async with message.channel.typing():
            ollama_path = r'C:\Users\Yuri\AppData\Local\Programs\Ollama\Ollama.exe'

            try:
                translation_prompt = f"Translate the following text to Japanese. Provide only the translation without any additional explanation or formatting: '{prompt}'"

                process = await asyncio.create_subprocess_exec(
                    ollama_path, 'run', 'gemma2:2b', translation_prompt,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    response = f"Error running ollama: {stderr.decode('utf-8')}"
                else:
                    response = stdout.decode('utf-8').strip()
            except Exception as e:
                response = f"Error running ollama: {e}"

            response = response.replace("failed to get console mode for stdout: The handle is invalid.", "").strip()
            response = response.replace("failed to get console mode for stderr: The handle is invalid.", "").strip()
            response = response.replace("Gemma", "Hyun (bot)") #PALITAN MO NALANG DIN YUNG NAME

            await message.channel.send(response)

client.run(TOKEN)
