# from allclass import *


MOVE = 0
SHOOT = 1
PICKUP = 2
RADIO = 3

RELAX = 0
ON_PLANE = 1
JUMPING = 2
MOVING = 3
SHOOTING = 4
PICKING = 5
MOVING_SHOOTING = 6
DEAD = 7
REAL_DEAD = 8

NOTHING = 0
FINDING = 1
TRY = 2


class AI:

    def __init__(self):
        self.status = NOTHING
        self.target = None

        pass

    def get_command(self, info):
        commands = []
        assert info.player_ID == 11
        if info.self.status == ON_PLANE or info.self.status == JUMPING:
            return []
        for item in info.items:
            if item.pos.distance < 1:
                commands.append(
                    {
                        'command_type': PICKUP,
                        'target': item.item_ID
                    }
                )
                break
        if len(info.self.bag):
            if not info.self.attack_cd:
                for player in info.others:
                    if player.player_ID > 7:
                        continue
                    commands.append(
                        {
                            'command_type': SHOOT,
                            'target': info.self.bag[0].item_ID,
                            "view_angle": player.pos.angle
                        }
                    )
                    break
        if not len(commands) and info.self.move_cd < 2:
            if self.status == TRY:
                for item_info in info.items:
                    if item_info.item_ID == self.target:
                        commands.append(
                            {
                                'command_type': MOVE,
                                "move_angle": item_info.pos.angle,
                                "view_angle": item_info.pos.angle,
                            }
                        )
                        break
                else:
                    if len(info.items):
                        info.items.sort(key=lambda x: x.pos.distance)
                        commands.append(
                            {
                                'command_type': MOVE,
                                "move_angle": info.items[0].pos.angle,
                                "view_angle": info.items[0].pos.angle,
                            }
                        )
                        self.target = info.items[0].item_ID
                        self.status = TRY
                    else:
                        commands.append(
                            {
                                'command_type': MOVE,
                                "move_angle": 29,
                                "view_angle": 29,
                            }
                        )
                        self.status = FINDING
            elif len(info.items):
                info.items.sort(key=lambda x: x.pos.distance)
                commands.append(
                    {
                        'command_type': MOVE,
                        "move_angle": info.items[0].pos.angle,
                        "view_angle": info.items[0].pos.angle,
                    }
                )
                self.target = info.items[0].item_ID
                self.status = TRY
            else:
                commands.append(
                    {
                        'command_type': MOVE,
                        "move_angle": 29,
                        "view_angle": 29,
                    }
                )
                self.status = FINDING
        return commands
