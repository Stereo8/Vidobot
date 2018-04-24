import discord
import asyncio
from things import youtube

class Vidobot(discord.Client):
    def __init__(self):

        self.OWNER_ID = '189726599556366336'
        self.BOT_PREFIX = '++,'
        self.queue = list()

        super().__init__()

    async def dodji(self, voice_channel: discord.Channel, text_channel: discord.Channel):
            try:
                return await self.join_voice_channel(voice_channel)
            except discord.errors.InvalidArgument:
                await self.send_message(text_channel, "Moraš da budeš u voice kanalu retardu.")

    async def umri(self, message: discord.Message):
        if message.author.id == self.OWNER_ID:
            await self.send_message(message.channel, "Okej :(")
            await self.close()
        else:
            await self.send_message(message.channel, "Ja se povinujem samo Vidu, ti si uljez!")

    def skip(self):
        self.queue[0][0].stop()

    def after_song(self):
        del self.queue[0]
        self.queue[0][0].start()
        # TODO: fucking song name

    async def pusti(self, message: discord.Message):
        # is the user even in a voice channel? is the bot? dodji() will take care of that.
        if self.is_voice_connected(message.server):
            voice_client = message.server.voice_client
        else:
            voice_client = await self.dodji(message.author.voice_channel, message.channel)
            if not self.is_voice_connected(message.server):
                return

        search_term = message.content.split(' ')[2:]
        await self.send_typing(message.channel)
        search_term = ' '.join(search_term)
        name = message.author.nick if message.author.nick is not None else message.author.name

        if len(self.queue) > 0 and self.queue[0][0].is_playing():
            player = await voice_client.create_ytdl_player(youtube.link(search_term), after=self.after_song)
            self.queue.append([player, message.channel, name])
            await self.send_message(message.channel, "Dodah **%s** u listu za *%s*..." % (player.title, name))
        else:
            player = await voice_client.create_ytdl_player(youtube.link(search_term), after=self.after_song)
            self.queue.append([player, message.channel, name])
            player.start()
            await self.send_message(message.channel, "Puštam **%s** za *%s*..." % (player.title, name))

    async def lista(self, message):
        q = ""
        for link in self.queue:
            q += "%s - **%s**, za *%s*\n" % (self.queue.index(link) + 1, link[0].title, link[2])
        await self.send_message(message.channel, q)

    async def on_message(self, message):
        print("<%s %s>[%s] %s" % (message.server, message.channel, message.author, message.content))
        args = message.content.split(" ")
        command = args[1]

        if args[0] == self.BOT_PREFIX:
            if command == "dodji":
                await self.dodji(message.author.voice_channel, message.channel)

            if command == "umri":
                await self.umri(message)

            if command == "pusti":
                await self.pusti(message)

            if command == "skip":
                self.skip()

            if command == "lista" or command == 'q':
                await self.lista(message)
