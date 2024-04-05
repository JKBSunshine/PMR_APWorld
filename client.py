from typing import TYPE_CHECKING, Set
import base64

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .data.data import *
from .Locations import location_name_to_id
from .items import item_id_prefix
from .data.LocationsList import location_groups, location_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class PaperMarioClient(BizHawkClient):
    game = "Paper Mario"
    system = "N64"
    patch_suffix = ".appm64"
    local_checked_locations: Set[int]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.autohint_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            game_names = await bizhawk.read(ctx.bizhawk_ctx, [(0x20, 0x14, "ROM"),
                                                              (TABLE_ADDRESS, 0x4, "ROM")])
            if game_names[0].decode("ascii") != "PAPER MARIO         ":
                return False

            if game_names[1] != MAGIC_VALUE:
                logger.info("This Paper Mario ROM is invalid.")
                return False

        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = False
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(AUTH_ADDRESS, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        try:

            read_state = await bizhawk.read(ctx.bizhawk_ctx, [(MODE_ADDRESS, 1, "RDRAM"),
                                                              (MF_START_ADDRESS, 0x221, "RDRAM"),
                                                              (GF_START_ADDRESS, 0x107, "RDRAM"),
                                                              (ITM_RCV_SEQ, 2, "RDRAM"),
                                                              (AREA_ADDRESS, 1, "RDRAM"),
                                                              (MAP_ADDRESS, 1, "RDRAM"),
                                                              (STAR_SPIRITS_COUNT, 1, "RDRAM")])

            # check for current state before sending or receiving anything
            game_mode = int.from_bytes(read_state[0], "big")

            if game_mode == GAME_MODE_WORLD:
                mod_flags = read_state[1]
                game_flags = read_state[2]
                received_items = int.from_bytes(bytearray(read_state[3]), "big")
                current_location = (int.from_bytes(bytearray(read_state[4]), "big"),
                                    int.from_bytes(bytearray(read_state[5]), "big"))
                star_spirits = int.from_bytes(bytearray(read_state[6]), "big")

                # RECEIVE ITEMS
                # Add item to buffer as u16 int
                if received_items < len(ctx.items_received):
                    next_item = ctx.items_received[received_items]
                    item_id = (next_item.item - item_id_prefix) << 16
                    await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                [(KEY_RECV_BUFFER, item_id.to_bytes(4, "big"), "RDRAM")],
                                                [(KEY_RECV_BUFFER, [0x00], "RDRAM"),
                                                 (ITM_RCV_SEQ, read_state[3], "RDRAM")])

                # SEND ITEMS
                mf_bytes = bytearray(mod_flags)
                gf_bytes = bytearray(game_flags)
                locs_to_send = set()

                # check through the checks table for checked checks
                for location, data in checks_table.items():
                    loc_id = location_name_to_id[location]
                    loc_val = False

                    # these flags are weird and require a helper function to do funny math, refer to doc linked in data
                    if data[0] == "MF":
                        loc_val = get_flag_value(data[0], data[1], mf_bytes)
                    elif data[0] == "GF":
                        loc_val = get_flag_value(data[0], data[1], gf_bytes)

                    if loc_val and loc_id in ctx.server_locations:
                        locs_to_send.add(loc_id)

                # Send locations if there are any to send
                if locs_to_send != self.local_checked_locations:
                    self.local_checked_locations = locs_to_send

                    if locs_to_send is not None:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

                # AUTO HINTING
                # Auto hint shop items so people know what they're paying for
                hints = []
                for loc in location_groups["AutoHint"]:
                    if loc not in self.autohint_locations:
                        # hint anything in the current map, area coordinates
                        if current_location == (location_table[loc][2], location_table[loc][3]):
                            # don't hint Rowf items you can't see/buy yet
                            if (location_table[loc][2], location_table[loc][3]) == (1, 2):
                                rowf_set = int(loc[31])
                                if rowf_set <= star_spirits + 1:
                                    hints.append(loc)
                            else:
                                hints.append(loc)

                # make sure we aren't hinting anything that's already been checked
                hints = [location_name_to_id[loc] for loc in hints if
                         location_name_to_id[loc] in ctx.missing_locations and
                         location_name_to_id[loc] not in ctx.locations_checked]

                # send request for hints
                if hints:
                    await ctx.send_msgs([{"cmd": "LocationScouts", "locations": hints, "create_as_hint": 2}])
                self.autohint_locations.update(hints)

                # GOAL CHECKING
                if not ctx.finished_game and (get_flag_value("GF", GOAL_FLAG, gf_bytes)):
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
