#!./venv/bin/python

from clock import CountdownClock
import discord
import io
import datetime
import asyncio
import logging
import json



with open('settings.json', 'r') as f:
    settings = json.load(f)

log = logging.getLogger('bot')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clock = CountdownClock.fromConfigYaml()

    async def sendDater(self, silent=True, force=False):

        now = datetime.datetime.now(tz=self.clock.timezone)

        if self.lastToday != now.date():
            self.lastToday = now.date()
            image = self.clock.GetStatusImage(now)
            imgfile = io.BytesIO()
            image.save(imgfile, format='PNG')
            self.image = imgfile.getvalue()

        channel = client.get_channel(settings['channel'])

        #clean out old messasges
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        validfound=None
        replied = set()
        unused = []
        async for message in channel.history(after=date, limit=1000):
            #print(message.created_at, message.author.name, message.content)
            if message.reference:
                replied.add(message.reference.message_id)
            if message.author == self.user and not message.content and message.attachments and message.attachments[0].filename=='countdown.png':
                if message.created_at.astimezone(self.clock.timezone).date() == now.date() and not force:
                    #be willing to trust an existing message that seems right and not print ours.  
                    #helps not make "new" messages when the bot gets restarted
                    #could fail on a message where the image is generated right before midnight but the post time is after midnight.
                    #we dont do this on force becasue if someone calls us it is to move the message up
                    validfound = message.id

#2.4        if message.author == self.user and not message.reactions and not message.stickers and not message.thread:
            if message.author == self.user and not message.reactions and not message.stickers and not channel.get_thread(message.id) :
               unused.append(message)

        for message in unused:
            if message.id not in replied and message.id != validfound:
#                print('would delete')
                await message.delete()
                
#        print('post')
        if validfound is None:
            file = discord.File(io.BytesIO(self.image), filename="countdown.png")
            await channel.send("", file=file, silent=silent)


    async def on_ready(self):
        log.info('Logged on as', self.user)
        self.lastToday=None
        await self.sendDater()

        async def periodic():
            while True:
                today = datetime.datetime.now(tz=self.clock.timezone).date()
                if self.lastToday != today:
                    log.info('periodic update')
                    await self.sendDater()
                    
                await asyncio.sleep(10)

        loop = asyncio.get_event_loop()
        task = loop.create_task(periodic())
        #task.cancel()


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if any(m==self.user for m in message.mentions):
#        if message.content == 'ping':
            log.info('user mention')
            await self.sendDater(force=True)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(settings['token'])

#https://discord.com/api/oauth2/authorize?client_id=1193953391290896477&permissions=108544&scope=bot


