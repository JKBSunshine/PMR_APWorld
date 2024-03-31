import asyncio
import copy
import orjson
import random
import time
from typing import TYPE_CHECKING, Optional, Dict, Set, Tuple
import uuid
import base64

from NetUtils import ClientStatus
from Options import Toggle
import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .data.data import *
from .Locations import location_name_to_id
from .items import item_id_prefix

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

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            game_names = await bizhawk.read(ctx.bizhawk_ctx, [(0x20, 0x14, "ROM"),
                                                              (TABLE_ADDRESS, 0x4, "ROM")])
            if game_names[0].decode("ascii") != "PAPER MARIO         ":
                return False

            if game_names[1] != MAGIC_VALUE:
                logger.info("This Paper Mario ROM is invalid. This error usually appears because the ROM is vanilla.")
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
                                                              (ITM_RCV_SEQ, 2, "RDRAM")])

            # check for current state before receiving items
            game_mode = int.from_bytes(read_state[0], "big")

            # Update the server with any new locations that have been checked
            mod_flags = read_state[1]
            game_flags = read_state[2]
            received_items = int.from_bytes(bytearray(read_state[3]), "big")

            # if we need to receive items, do so, so long as we're loaded
            # any game mode which occurs after loading a file is fine, use overworld for now since that's when items
            # will actually be given to Mario anyways
            if game_mode == GAME_MODE_WORLD and received_items < len(ctx.items_received):
                next_item = ctx.items_received[received_items]
                item_id = next_item.item - item_id_prefix
                item_id = item_id << 16
                await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                            [(KEY_RECV_BUFFER, item_id.to_bytes(4, "big"), "RDRAM")],
                                            [(KEY_RECV_BUFFER, [0x00], "RDRAM")])


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
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(locs_to_send)
                    }])

            # send game clear if flag is set
            if not ctx.finished_game and (get_flag_value("GF", GOAL_FLAG, gf_bytes)):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
