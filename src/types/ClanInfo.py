class ClanInfo:
    def __init__(self, name, member_count, clan_open, update_time):
        self.name = name
        self.member_count = member_count
        self.clan_open = clan_open
        self.update_time = update_time

    def is_clan_open(self):
        if not self.clan_open:
            return False

        return self.member_count < 90

    def is_clan_open_str(self):
        return 'Open' if self.is_clan_open() else 'Closed'

    def pretty_print(self):
        return '**' + self.name.capitalize() + '** (' + ('<:Greentick:1069642256103002214>' if self.is_clan_open() else '<:Redcross:1069642390052278292>') + '): ' + str(self.member_count)
