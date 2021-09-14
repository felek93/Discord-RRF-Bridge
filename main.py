import urllib.request, json 
import discord
import os

MaxMessageLength = 2000

urlIP = 'http://<printer ip address>'
urlGCode = urlIP + '/rr_gcode?gcode='
urlModel = urlIP + '/rr_model?flags=d99fn'
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

    if message.content.startswith('@status'):
        with urllib.request.urlopen(urlModel) as url:
            data = json.loads(url.read().decode())
            await message.channel.send('Printer status: ' + data['result']['state']['status'])
            return

    with urllib.request.urlopen(urlGCode + message.content.replace(' ','%20')) as url:
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

client.run(TOKEN)

