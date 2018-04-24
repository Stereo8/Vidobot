import requests
import json


class FortniteStats(object):
    def __init__(self):
        self.kills = 0
        self.matches_played = 0
        self.last_match = ""
        self.wins = 0
        self.top10 = 0
        self.top25 = 0
        self.deaths = 0
        self.kpd = 0.0
        self.kpm = 0.0
        self.tpm = 0.0
        self.score = 0
        self.win_rate = 0.0


class FortnitePlayer:
    def __init__(self, name):
        url = "https://fortnite.y3n.co/v2/player/" + name + '/'
        headers = {"X-Key": "0xNaeXTJmx8ps6XLQgEc"}

        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            raise FileNotFoundError
        if response.status_code != 200:
            raise RuntimeError

        parsed = json.loads(response.text)
        stats = parsed['br']['stats']['pc']

        self.display_name = parsed['displayName']

        self.solo = FortniteStats()

        self.solo.kills = stats['solo']['kills']
        self.solo.matches_played = stats['solo']['matchesPlayed']
        self.solo.last_match = stats['solo']['lastMatch']
        self.solo.wins = stats['solo']['wins']
        self.solo.top10 = stats['solo']['top10']
        self.solo.top25 = stats['solo']['top25']
        self.solo.deaths = stats['solo']['deaths']
        self.solo.kpd = stats['solo']['kpd']
        self.solo.kpm = stats['solo']['kpm']
        self.solo.tpm = stats['solo']['tpm']
        self.solo.score = stats['solo']['score']
        self.solo.win_rate = stats['solo']['winRate']

        self.duo = FortniteStats()

        self.duo.kills = stats['duo']['kills']
        self.duo.matches_played = stats['duo']['matchesPlayed']
        self.duo.last_match = stats['duo']['lastMatch']
        self.duo.wins = stats['duo']['wins']
        self.duo.top5 = stats['duo']['top5']
        self.duo.top12 = stats['duo']['top12']
        self.duo.deaths = stats['duo']['deaths']
        self.duo.kpd = stats['duo']['kpd']
        self.duo.kpm = stats['duo']['kpm']
        self.duo.tpm = stats['duo']['tpm']
        self.duo.score = stats['duo']['score']
        self.duo.win_rate = stats['duo']['winRate']
        
        self.squad = FortniteStats()

        self.squad.kills = stats['squad']['kills']
        self.squad.matches_played = stats['squad']['matchesPlayed']
        self.squad.last_match = stats['squad']['lastMatch']
        self.squad.wins = stats['squad']['wins']
        self.squad.top3 = stats['squad']['top3']
        self.squad.top6 = stats['squad']['top6']
        self.squad.deaths = stats['squad']['deaths']
        self.squad.kpd = stats['squad']['kpd']
        self.squad.kpm = stats['squad']['kpm']
        self.squad.tpm = stats['squad']['tpm']
        self.squad.score = stats['squad']['score']
        self.squad.win_rate = stats['squad']['winRate']

        self.wins = self.solo.wins + self.duo.wins + self.squad.wins
        self.winrate = (self.solo.win_rate + self.duo.win_rate + self.squad.win_rate) / 3
        self.matches_played = self.solo.matches_played + self.duo.matches_played + self.squad.matches_played
