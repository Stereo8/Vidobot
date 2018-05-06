import discord
from things import fortnite
from things import youtube
from things import paki
from things import ph
from things import status
import time


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

    async def pusti(self, message: discord.Message, **kwargs):
        # is the user even in a voice channel? is the bot? dodji() will take care of that.
        if self.is_voice_connected(message.server):
            voice_client = message.server.voice_client
        else:
            voice_client = await self.dodji(message.author.voice_channel, message.channel)
            if not self.is_voice_connected(message.server):
                return

        try:
            search_term = kwargs['search_term']
        except KeyError:
            search_term = message.content.split(' ')[2:]
            search_term = ' '.join(search_term)
        await self.send_typing(message.channel)
        name = message.author.nick if message.author.nick is not None else message.author.name

        if len(self.queue) > 0 and self.queue[0][0].is_playing():
            try:
                player = await voice_client.create_ytdl_player(youtube.link(search_term), after=self.after_song)
            except Exception:
                await self.send_message(message.channel, "Sjebalo se nešto kod traženja, pokušaj sa linkom ili "
                                                         "drugačije napiši")
                return
            self.queue.append([player, message.channel, name])
            await self.send_message(message.channel, "Dodah **%s** u listu za *%s*..." % (player.title, name))
        else:
            try:
                player = await voice_client.create_ytdl_player(youtube.link(search_term), after=self.after_song)
            except Exception:
                await self.send_message(message.channel, "Sjebalo se nešto kod traženja, pokušaj sa linkom ili "
                                                         "drugačije napiši")
                return
            self.queue.append([player, message.channel, name])
            player.start()
            await self.send_message(message.channel, "Puštam **%s** za *%s*..." % (player.title, name))

    async def pesme(self, message, search_term):

        def check(msg):
                if int(msg.content) in range(0, 5):
                    return True

        results = youtube.links(search_term)
        delmes = await self.send_message(message.channel, "Izaberi jedan od izbora: \n**1.** %s \n**2.** %s \n**3.** "
                                                          "%s "
                                                          "\n**4.** %s \n**5.** %s " % (
                                         results[0][1], results[1][1], results[2][1], results[3][1], results[4][1]))
        try:
            msg = await self.wait_for_message(timeout=15.0, author=message.author, channel=message.channel, check=check)
        except ValueError:
            self.send_message(message.channel, "Debilčino, rekao sam broj od jedan do pet.")
            return

        await self.pusti(message, search_term=results[int(msg.content) - 1])
        await self.delete_message(delmes)
        await self.delete_message(msg)

    async def lista(self, message):
        q = ""
        for link in self.queue:
            q += "%s - **%s**, za *%s*\n" % (self.queue.index(link) + 1, link[0].title, link[2])
        await self.send_message(message.channel, q)

    async def mars(self, message):
        await self.send_message(message.channel, "Odjebavam iz *%s*..." % self.voice_client_in(
                message.server).channel.name)
        await self.voice_client_in(message.server).disconnect()

    async def fortnite(self, name, message):
        try:
            player = fortnite.FortnitePlayer(name)
        except FileNotFoundError:
            await self.send_message(message.channel, "Igrač nije pronađen!")
        except RuntimeError:
            await self.send_message(message.channel, "Nekakva grdna greška se dogodila... :cold_sweat:")
        else:

            embed = discord.Embed(title="Fortnite stats od %s" % (player.display_name),
                                  description="%s - Pobede - %d - Winrate - %.2f%% - Mečevi - %d" % (
                                      player.display_name, player.wins, player.winrate, player.matches_played),
                                  color=0x00ff00)
            embed.add_field(name='Solo',
                            value='K/D - **%.2f** | Pobede - **%d** | Killovi - **%d** | Winrate - **%.2f%%** |  Mečevi - '
                                  '**%d**' % (
                                      player.solo.kpd, player.solo.wins, player.solo.kills, player.solo.win_rate,
                                      player.solo.matches_played))
            embed.add_field(name='Duo',
                            value='K/D - **%.2f** | Pobede - **%d** | Killovi - **%d** | Winrate - **%.2f%%** |  Mečevi - '
                                  '**%d**' % (player.duo.kpd, player.duo.wins, player.duo.kills, player.duo.win_rate,
                                              player.duo.matches_played))
            embed.add_field(name='Squad',
                            value='K/D - **%.2f** | Pobede - **%d** | Killovi - **%d** | Winrate - **%.2f%%** |  Mečevi - '
                                  '**%d**' % (
                                      player.squad.kpd, player.squad.wins, player.squad.kills, player.squad.win_rate,
                                      player.squad.matches_played))
            embed.set_footer(text="powered by Vidobot++™")
            await self.send_message(message.channel, embed=embed)

    async def purge(self, message: discord.Message, number):
        if message.author.permissions_in(message.channel).manage_messages:
            try:
                await self.purge_from(message.channel, limit=int(number))
            except ValueError:
                await self.send_message(message.channel, "Napiši broj poruka slovima mentolu")
        else:
            await self.send_message(message.channel, "Nemaš ti tu moć, smrtniče ubogi")

    async def kikuj(self, message):
        if message.author.server_permissions.kick_members and len(message.mentions) > 0:
            for member in message.mentions:
                try:
                    await self.kick(member)
                    await self.send_message(message.channel, "Kikovah %s!" % (member.name))
                except discord.Forbidden:
                    await self.send_message(message.channel, "Ne mogu da kikujem %s!" % (member.name))
        elif not message.author.server_permissions.kick_members:
            await self.send_message(message.channel, "Nemaš ti tu moć, smrtniče ubogi")
        elif len(message.mentions) == 0:
            await self.send_message(message.channel, "Moraš da ih menšnuješ tebra")

    async def banuj(self, message):
        if message.author.server_permissions.ban_members and len(message.mentions) > 0:
            for member in message.mentions:
                try:
                    await self.ban(member)
                    await self.send_message(message.channel, "Banovah %s!" % (member.name))
                except discord.Forbidden:
                    await self.send_message(message.channel, "Ne mogu da banujem %s!" % (member.name))
        elif not message.author.server_permissions.ban_members:
            await self.send_message(message.channel, "Nemaš ti tu moć, smrtniče ubogi.")
        elif len(message.mentions) == 0:
            await self.send_message(message.channel, "Moraš da ih menšnuješ tebra.")

    async def paki(self, channel: discord.Channel):
        await self.send_message(channel, "Naš drugar Paki ima *%s* sabskrajbera! Svaka čast!" % (
            paki.pakijev_subcount()))

    async def reciga(self, message: discord.Message):
        voice = await self.dodji(message.author.voice_channel, message.channel)
        player = voice.create_ffmpeg_player('things/ALUBULJUE.mp3')
        player.volume = 2
        player.start()
        time.sleep(1.6)
        await voice.disconnect()
        await self.delete_message(message)

    async def pornhub(self, channel: discord.Channel):
        await self.send_message(channel, ph.comment())

    async def status(self, message):
        await self.send_message(message.channel, "{0} \n"
                                                 "{1} \n"
                                                 "{2} \n".format(status.cpu(), status.memory(), status.load_avg()))

    async def on_message(self, message: discord.Message):
        print("<%s %s>[%s] %s" % (message.server, message.channel, message.author, message.content))
        args = message.content.split(" ")
        if len(args) < 2:
            return
        else:
            command = args[1]

        if args[0] == self.BOT_PREFIX:
            if command == "dodji":
                await self.dodji(message.author.voice_channel, message.channel)

            if command == "umri":
                await self.umri(message)

            if command == "pusti":
                await self.pusti(message)

            if command == "youtube":
                await self.pesme(message, ' '.join(args[2:]))

            if command == "skip":
                self.skip()

            if command == "lista" or command == 'q':
                await self.lista(message)

            if command == "mars" or command == "mrs":
                await self.mars(message)

            if command == "fortnite":
                await self.fortnite(' '.join(args[2:]), message)

            if command == "purge":
                await self.purge(message, args[2])

            if command == "kikuj":
                await self.kikuj(message)

            if command == "banuj":
                await self.banuj(message)

            if message.content.startswith(self.BOT_PREFIX + " reci ga"):
                await self.reciga(message)

            if command.startswith("paki"):
                await self.paki(message.channel)

            if command == "pornhub":
                await self.pornhub(message.channel)

            if command == "status":
                await self.status(message)
