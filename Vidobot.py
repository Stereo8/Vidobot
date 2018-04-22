import discord
import asyncio


class Vidobot(discord.Client):
    def __init__(self):
        self.OWNER_ID = '189726599556366336'

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


    async def pusti(self, message: discord.Message):
        if self.is_voice_connected(message.server):
            voice_client = message.server.voice_client
        else:
            voice_client = await self.dodji(message.author.voice_channel, message.channel)
            if not self.is_voice_connected(message.server):
                return

        player = await voice_client.create_ytdl_player("https://www.youtube.com/watch?v=PjqKPHZJgF0")
        player.start()


    async def on_message(self, message):
        print("<%s %s>[%s] %s" % (message.channel, message.channel, message.author, message.content))
        args = message.content.split(" ")
        command = args[1]

        if command == "dodji":
            await self.dodji(message.author.voice_channel, message.channel)

        if command == "umri":
            await self.umri(message)

        if command == "pusti":
                await self.pusti(message)

