from allclass import *
import proto.platform_pb2 as platform

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
GUN = 3


class AI:

    def __init__(self):
        self.status = NOTHING
        self.target = None

        pass

    def no_gun(self, infos):
        commands = []
        for item in infos.items:
            if item.pos.distance < 1:
                commands.append(
                    {
                        'command_type': PICKUP,
                        'target': item.item_ID,
                        'other': 0,
                    }
                )
                self.status = NOTHING
                break

        if len(infos.self.bag):
            if not infos.self.attack_cd:
                for player in infos.others:
                    if player.player_ID > 7:
                        continue
                    commands.append(
                        {
                            'command_type': SHOOT,
                            'target': infos.self.bag[0].item_ID,
                            "view_angle": player.pos.angle,
                            'other': 0
                        }
                    )
                    break

        if not len(commands) and infos.self.move_cd < 2:
            if self.status == TRY:
                for item_info in infos.items:
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
                    if len(infos.items):
                        infos.items.sort(key=lambda x: x.pos.distance)
                        commands.append(
                            {
                                'command_type': MOVE,
                                "move_angle": infos.items[0].pos.angle,
                                "view_angle": infos.items[0].pos.angle,
                            }
                        )
                        self.target = infos.items[0].item_ID
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
            elif len(infos.items):
                infos.items.sort(key=lambda x: x.pos.distance)
                commands.append(
                    {
                        'command_type': MOVE,
                        "move_angle": infos.items[0].pos.angle,
                        "view_angle": infos.items[0].pos.angle,
                    }
                )
                self.target = infos.items[0].item_ID
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

    def has_gun(self, infos):
        commands = []
        aim = None
        for other in infos.others:
            if other.status != DEAD:
                aim = other
        if aim:
            commands.append(
                {
                    'command_type': SHOOT,
                    'target': infos.self.bag[0].item_ID,
                    "view_angle": aim.pos.angle,
                    'other': 0
                }
            )
        else:
            pos = position.Position(infos.self.pos.x, infos.self.pos.y)
            dist, angle = pos.get_polar_position(position.angle_to_position(infos.self.view_angle),
                                                 position.Position(100, 200))
            if dist > 20 or 20 < angle < 340:
                commands.append(
                    {
                        'command_type': MOVE,
                        "move_angle": angle,
                        "view_angle": angle,
                    }
                )
            else:
                commands.append(
                    {
                        'command_type': MOVE,
                        "move_angle": 119,
                        "view_angle": 119,
                    }
                )
        return commands

    def get_command(self, infos):
        infos = platform.PlayerInfo.FromString(infos)
        assert infos.player_ID == 11
        if infos.self.status == ON_PLANE or infos.self.status == JUMPING:
            commands = []
        elif len(infos.self.bag):
            commands = self.has_gun(infos)
        else:
            commands = self.no_gun(infos)
        return commands
