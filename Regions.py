from BaseClasses import Region, MultiWorld


class PMRegion(Region):
    game: str = "Paper Mario"

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super(PMRegion, self).__init__(name, player, multiworld)
        self.map_name = None
        self.map_id = None
        self.area_id = None
