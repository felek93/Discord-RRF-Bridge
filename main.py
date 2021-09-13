import urllib.request, json 
import discord
import os

MaxMessageLength = 2000

urlIP = 'http://<printer ip address>'
urlGCode = urlIP + '/rr_gcode?gcode='
urlReply = urlIP + '/rr_reply'

TOKEN = '<yout discord bot token>'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #print(message.content)
    with urllib.request.urlopen(urlGCode + message.content) as url:
        data = json.loads(url.read().decode())
        #print(data)
    
    with urllib.request.urlopen(urlReply) as url:
        reply = url.read().decode()
        size = len(reply)
        if size > 0:
            if (size < MaxMessageLength):
                await message.channel.send(reply)
            else:
                # Max message size is 2000, so we need to send multiple message
                index = size / MaxMessageLength
                i = 0
                while i < index:
                    await message.channel.send(reply[i * MaxMessageLength : i * MaxMessageLength + MaxMessageLength])
                    i += 1

    if message.content.startswith('@status'):
        await message.channel.send('... future ...')

client.run(TOKEN)

