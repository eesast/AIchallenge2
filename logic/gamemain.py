#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass import *
import proto.interface_pb2 as interface
import proto.platform_pb2 as platform
from random import randrange
from json import load
import math
import time
import struct

#   here define a debug level variable to debug print-oriented
#   remember: here is just a initial level for logic
#   platform may give another number in game_init
PRINT_DEBUG = 21


#   level 1: only print illegal information
#   level 2: also print some adjustment
#   level 3: print illegal instruction for wrong format
#   level 4: print illegal instruction for wrong logic
#   level 5: print illegal instruction for current status
#   level 6: print real dead information
#   level 7: print dead information

#   level 8: give all players' jumping information
#   level 9: print initialize information for parachuting

#   level 10: print turns

#   level 13: print damage information
#   level 14: print player's failed moving
#   level 15: print player's new position after each move
#   level 16: print player's new pick-up
#   level 17: print circle dynamic changing

#   level 20: print player's view for other players
#   level 21: print player's view for items

#   level 25: print player's view for landforms

#   level 29: print all non-redundant commands for each frame
#   level 30: print all commands for each frame

#   level 50: print data length for proto

#   level 100: will give all information you can imagine, including config file

class GameMain:
    # if not specified, platform needn't this class's members
    map_size = 1000
    playback_file_path = None

    def __init__(self):

        # it's more like a define instead of an initialization
        self.die_order = []  # save the player's dying order
        self.die_list = []  # die order in this frame for platform
        self.map_items = [[[] for i in range(16)] for j in range(16)]  # try to divide map into 256 parts
        self.map = terrain.Map()

        self.all_players = []  # save all teams and players
        self.all_bullets = []
        self.all_sounds = []
        self.all_wild_items = {}
        self.all_info = {}  # save all information for platform
        self.all_commands = {"move": {}, "shoot": {}, "pickup": {}, "radio": {}}

        self.number_to_team = {}  # use a number to find a team
        self.number_to_player = {}  # use a number to find a player
        self.__start_position, self.__over_position = None, None
        self.__turn = 0
        self.poison = None

        # initialize debug level for logic to use directly and for platform to change it
        self.__debug_level = PRINT_DEBUG

        return

    def set_debug_level(self, level):
        if level:
            self.__debug_level = level
        return

    def load_data(self, file_path, file_name):
        if file_path[-1] != '/' and file_path[-1] != '\\':
            file_path = file_path + '/'
        # first load some global information
        with open(file_path + file_name) as config:
            global_config = load(config)
        self.print_debug(100, global_config)

        # then load some module data here
        self.print_debug(100, character.Character.load_data(file_path, global_config["CHARACTER_FILE_PATH"]))
        self.print_debug(100, item.Item.load_data(file_path, global_config["ITEM_FILE_PATH"]))
        self.print_debug(100, sound.Sound.load_data(file_path, global_config["SOUND_FILE_PATH"]))

        # here load map data
        self.__load_map(file_path, global_config["MAP_FILE_PATH"])

        # for play back file
        playback_child_path = global_config["PLAYBACK_FILE_PATH"] + time.strftime("%Y%m%d_%H'%M'%S") + ".pb"
        GameMain.playback_file_path = file_path + playback_child_path
        open(GameMain.playback_file_path, 'wb').close()  # create the new playback file

        # for circle data
        self.print_debug(100, self.poison.load_data(file_path, global_config["CIRCLE_FILE_PATH"]))

    def map_init(self):
        # here should give some items randomly according to occurrence
        # but for debug just give some same guns
        num = 20
        for i in range(num):
            for j in range(num):
                pos = position.Position(1000 // num // 2 + i * 1000 // num, 1000 // num // 2 + j * 1000 // num)
                self.all_wild_items[item.Item.add('RIFLE', pos)] = item.Item.all_data['RIFLE']['number'], pos
        # now i add 10000 well-distributed  rifle guns
        return

    def unwrap_commands(self, commands):
        # here unwrap all players' commands
        self.all_commands["move"].clear()
        self.all_commands["shoot"].clear()
        self.all_commands["pickup"].clear()
        self.all_commands["radio"].clear()
        # commands format: { playerID: [{"command_tye":type, "target":
        # ID, "move_angle": angle, "view_angle": angle, "other": data}]}}

        self.print_debug(30, commands)
        for playerID, player_commands in commands.items():
            for command in player_commands:
                command_type = command["command_type"]
                if command_type == character.MOVE:
                    self.all_commands["move"][playerID] = command["move_angle"], command["view_angle"]
                elif command_type == character.SHOOT:
                    self.all_commands["shoot"][playerID] = \
                        command["view_angle"], command["target"], command["other"]
                elif command_type == character.PICKUP:
                    self.all_commands["pickup"][playerID] = command["target"], command["other"]
                elif command_type == character.RADIO:
                    self.all_commands["radio"][playerID] = command["target"], command["other"]
                else:
                    # if command_type isn't correct, it will be ignored
                    continue
        self.print_debug(29, "unwrap_command successfully")
        self.print_debug(29, self.all_commands)
        return

    def __load_map(self, parent_path, map_file_path):
        self.map.initialize(terrain.Area.load_data(parent_path, map_file_path))
        self.map_size = GameMain.map_size
        self.poison = circle.Circle(self.map_size)

    def alive_teams(self):
        teams = []
        for team in self.all_players:
            alive = []
            for player in team:
                # check if there is at least one alive player in this team
                if player.health_point > 0:
                    alive.append(player.number)
                    break
                else:
                    continue
            if len(alive):
                teams.append(alive)
        return teams

    def generate_route(self):
        # a function to get random position for airplane's route
        def random_route():
            # a random method to get an elegant route
            length = self.map_size
            perimeter = 4 * length
            start_number = randrange(0, length * 4)
            parameter_start = int(start_number + 1.5 * length)
            parameter_over = int(start_number + 2.5 * length)
            over_number = randrange(parameter_start, parameter_over) % perimeter
            return get_position(start_number), get_position(over_number)

        # a function to get position from a parameter length
        def get_position(parameter):
            length = self.map_size

            # calculate which edge is aim point on
            edge = parameter // length
            if edge == 0:
                x, y = parameter % length, 0
            elif edge == 1:
                x, y = length, parameter % length
            elif edge == 2:
                x, y = length - parameter % length, length
            elif edge == 3:
                x, y = 0, length - parameter % length
            else:
                # if parameter isn't in the right range, it may work, although not supposed to
                return get_position((parameter + 4 * length) % (4 * length))
            return position.Position(x, y)

        # first get two position for the air route
        self.__start_position, self.__over_position = random_route()

        # for debug, but it also can be used in  if needed
        print("the route's start position is", self.__start_position, "and its over position is", self.__over_position)
        return self.__start_position, self.__over_position

    # jump from airplane before start fighting
    def parachute(self, information):
        # a function to process position data from platform
        def unwrap():
            # here I get all players information and players' aim positions via data from platform
            if not isinstance(information, dict):
                raise Exception("wrong information!")

            for player_number, player_information in information.items():
                team_number = player_information['team']
                new_vocation = player_information['vocation']

                if not isinstance(player_information, dict):
                    raise Exception("wrong team_information!")
                if not isinstance(team_number, int):
                    raise Exception("wrong team_number!")

                new_team = []
                # if this is the first player in this team, add team information
                if self.number_to_team.get(team_number, None) is None:
                    self.all_players.append(new_team)
                    self.number_to_team[team_number] = new_team
                else:
                    new_team = self.number_to_team[team_number]

                # first judge if this vocation is legal
                if not 0 <= new_vocation <= character.Character.VOCATION_COUNT:
                    self.print_debug(1, "number", player_number, "choose illegal vocation", new_vocation)
                    # if illegal, change it as zero
                    new_vocation = 0

                # then ensure it hasn't been chosen, or I will give one
                for player_check in self.number_to_team[team_number]:
                    if new_vocation == player_check.vocation:
                        self.print_debug(1, "player", player_number, "choose repeated vocation", new_vocation, end='')
                        new_vocation = (new_vocation + 1) % character.Character.VOCATION_COUNT
                        self.print_debug(1, ", now it's adjusted to", new_vocation)

                new_player = character.Character.add_character(player_number, new_vocation)
                new_player.team = team_number
                new_player.land_position = position.Position(player_information['position'])
                if not new_player.land_position.good(self.map_size):  # for illegal aim, auto fall in the end
                    self.print_debug(1, "number", player_number, "choose illegal aim", new_player.land_position)
                    new_player.land_position = self.__over_position
                new_team.append(new_player)
                self.number_to_player[player_number] = new_player
            return

        def get_pedal(aim_position, number=-1):
            aim_x, aim_y = aim_position.x, aim_position.y
            a = position.delta_y(self.__over_position, self.__start_position)
            b = - position.delta_x(self.__over_position, self.__start_position)
            c = position.cross_product(self.__over_position, self.__start_position)
            x = (b * b * aim_x - a * b * aim_y - a * c) / (a * a + b * b)
            y = (a * a * aim_y - a * b * aim_x - b * c) / (a * a + b * b)
            aim = position.Position(x, y)
            # if the pedal isn't in the map, player must jump at begin or end
            if x < 0 or y < 0 or x > self.map_size or y > self.map_size:
                self.print_debug(2, "player", number, "aimed", aim_position, "pedal is", aim, end='')
                aim = self.__start_position if aim.distance2(self.__start_position) < aim.distance2(
                    self.__over_position) else self.__over_position
                self.print_debug(2, "now it has been adjusted to", aim)
            return aim

        def get_proto_data():
            data = interface.InitialInfo()
            data.start.x, data.start.y = self.__start_position.x, self.__start_position.y
            data.over.x, data.over.y = self.__over_position.x, self.__over_position.y
            for each_team in self.all_players:
                for each_player in each_team:
                    player_info = data.players.add()
                    player_info.id = each_player.number
                    player_info.team = each_player.team
                    player_info.vocation = each_player.vocation
                    player_info.HP_max = int(each_player.health_point)  # now HP == HP_max
            return data

        self.print_debug(9, 'parachute:' + str(information))

        # here unwrap players' information and their land positions
        unwrap()

        # I just got teams information for the first time, now save them
        for team in self.all_players:
            for player in team:
                if not isinstance(player, character.Character):
                    raise Exception("wrong object for dict number_to_player, get a", type(player))
                # I hope it's a pointer, otherwise it's a huge bug
                player.jump_position = get_pedal(player.land_position, player.number)
                player.move_direction = (self.__over_position - self.__start_position).unitize()
                player.position = self.__start_position
                player.move_speed = character.Character.AIRPLANE_SPEED
                player.move_cd = int((player.jump_position - self.__start_position).length() / player.move_speed + 1)
                player.face_direction = player.move_direction
                player.status = character.Character.ON_PLANE
                # meanwhile deal with information dictionary
                self.all_info[player.number] = info.Information(player)

        # output data for interface
        self.write_playback(get_proto_data())

        # now everything down, main operation starts
        # return first turn's information
        return self.refresh()

    def refresh(self):  # refresh a new frame according to the orders

        def instructions():
            # pick up
            for player_number, command in self.all_commands['pickup'].items():
                picked_item = item.Item.all_items[command[0]]
                player = character.Character.all_characters[player_number]
                if self.all_wild_items.get(picked_item.id, None) is None:
                    self.print_debug(4, 'player', player_number, 'try to pick item not existing or belonging to others')
                if picked_item.id not in self.all_info[player_number].items:
                    self.print_debug(4, 'player', player_number, 'try to pick item out of view')
                elif not player.position.pick_accessible(picked_item.position):
                    self.print_debug(4, 'player', player_number, "tyr to pick item beyond pick range")
                else:
                    # now this player can get it
                    player.bag[picked_item.item_type] = player.bag.setdefault(picked_item.item_type, 0) + \
                                                        picked_item.durability
                    self.all_wild_items.pop(picked_item.id)
                    item.Item.remove(picked_item.id)
                    character.Character.all_characters[player_number].change_status(character.Character.PICKING)
                    self.print_debug(16, 'player', player_number, 'pick up', picked_item.data['name'], picked_item.id)
                    # maybe we should deal with command['other'], now ignore it
                    pass
            # move
            for player_id, command in self.all_commands['move'].items():
                move_angle, view_angle = command
                player = character.Character.all_characters[player_id]
                if not player.command_status_legal(character.MOVE):
                    self.print_debug(5, 'player', player_id, 'try to move but not in right status')
                elif not 0 <= move_angle <= 360:
                    self.print_debug(3, 'player', player_id, 'give wrong move angle as', move_angle)
                elif not 0 <= view_angle <= 360:
                    self.print_debug(3, 'player', player_id, 'give wrong view angle as', view_angle)
                else:  # now do it
                    player.change_status(character.Character.MOVING)
                    basic_angle = player.face_direction.get_angle()
                    player.face_direction = position.angle_to_position(view_angle + basic_angle)
                    player.move_direction = position.angle_to_position(move_angle + basic_angle)
            # shoot
            for player_id, command in self.all_commands['shoot'].items():
                view_angle, item_type, other = command
                player = character.Character.all_characters[player_id]
                rest = player.bag.get(item_type, 0)
                if player.shoot_cd:
                    self.print_debug(4, 'player', player_id, 'try to shoot with', player.shoot_cd, ' shoot cd')
                elif not rest:
                    self.print_debug(4, 'player', player_id, 'try to use weapon without durability')
                elif item.Item.all_data[item_type]['type'] != 'weapon':
                    self.print_debug(4, 'player', player_id, 'try to use not weapon-like item to shoot')
                elif not 0 <= view_angle <= 360:
                    self.print_debug(3, 'player', player_id, 'give wrong attack angle as', view_angle)
                else:  # now shoot
                    player.bag[item_type] -= 1
                    view_angle += player.face_direction.get_angle()  # correct relative angle to absolute angle
                    if view_angle >= 360:
                        view_angle -= 360
                    player.shoot_cd = item.Item.all_data[item_type]['cd']
                    player.face_direction = position.angle_to_position(view_angle)
                    player.change_status(character.Character.SHOOTING)
                    self.all_bullets.append((player.position, view_angle, item_type, player_id, None))
                    # here should deal with other parameter, just put off

                    # here deal with gun sound
                    for team in self.all_players:
                        for receiver in team:
                            if receiver is player:
                                continue
                            if abs(receiver.position - player.position) < sound.Sound.farthest['gun']:
                                self.all_sounds.append(sound.Sound(sound.Sound.GUN_SOUND, receiver.number,
                                                                   player.position,
                                                                   abs(player.position - receiver.position)))
            # radio
            for emitter_id, command in self.all_commands['radio'].items():
                # here receiver_id include some other data for signalman, awaiting to process
                receiver_id, data = command
                emitter = character.Character.all_characters[emitter_id]
                receiver = character.Character.all_characters[receiver_id]
                self.all_sounds.append(sound.Sound(sound.Sound.RADIO_VOICE, receiver_id, emitter.position,
                                                   abs(emitter.position - receiver.posistion), emitter_id, data))
            return

        def move():
            for team in self.all_players:
                for player in team:
                    self.all_info[player.number].clear()
                    past_position = player.position
                    if player.move():
                        if player.is_flying() or player.is_jumping() or self.map.stand_permitted(player.position,
                                                                                                 player.radius):
                            self.print_debug(15, 'player', player.number, 'move to', player.position)
                            if player.move_cd == 1 and player.can_make_footsteps():
                                # for foot step sound
                                for _team in self.all_players:
                                    for receiver in _team:
                                        if receiver is player:
                                            # player won't get footsteps by himself
                                            continue
                                        if abs(receiver.position - player.position) < sound.Sound.farthest['footstep']:
                                            self.all_sounds.append(
                                                sound.Sound(sound.Sound.FOOTSTEP_SOUND, receiver.number,
                                                            player.position, abs(player.position - receiver.position)))

                        else:
                            self.print_debug(14, 'player', player.number, 'failed to move to', player.position)
                            player.position = past_position
                            input()

        def attack():
            bullets = self.all_bullets
            for index in range(len(bullets)):
                pos, view_angle, item_type, player_id, hit_id = bullets[index]
                shortest = None
                data = item.Item.all_data[item_type]
                for team in self.all_players:
                    if character.Character.all_characters[player_id] in team:
                        continue
                    for player in team:
                        if not player.can_be_hit():
                            continue
                        dist, delta = pos.get_polar_position(position.angle_to_position(view_angle), player.position)
                        delta = 0 if delta > 360 else 360 - delta if delta > 180 else delta
                        if delta < 2.5:
                            if dist > data['range']:
                                continue
                            if not shortest or shortest < dist:
                                # modify hit player
                                shortest = dist
                                bullets[index] = pos, view_angle, item_type, player_id, player.number
            return

        def damage():
            bullets = self.all_bullets
            for index in range(len(bullets)):
                pos, view_angle, item_id, player_id, hit_id = bullets[index]
                if hit_id is not None:
                    direction = position.angle_to_position(view_angle)
                    target = character.Character.all_characters[player_id].position
                    dist = abs(position.cross_product(direction, target - pos))
                    data = item.Item.get_data_by_item_id(item_id)
                    value = math.exp(-dist * 100 / data['range']) * data['damage']
                    character.Character.all_characters[hit_id].health_point -= value

                    self.print_debug(13, 'player', player_id, data['name'], value, 'damage to player', hit_id)
                else:
                    if item.Item.all_items[item_id].item_type == 1:
                        bullets[index] = pos, view_angle, item_id, player_id, True

            self.all_bullets = [bullet for bullet in bullets if bullet[4] is None]
            return

        def die():
            self.die_list = []
            for team in self.all_players:
                for player in team:
                    if self.poison.safe(player):
                        if player.can_be_hit() and player.health_point <= 0:
                            player.health_point = 0
                            player.change_status(character.Character.DEAD)
                            self.print_debug(7, 'player', player.number, 'dead')
                    else:
                        player.health_point -= self.poison.damage_per_frame
                        self.print_debug(13, 'circle caused', self.poison.damage_per_frame, 'damage to', player.number)
                        if player.can_be_hit() and player.health_point <= 0:
                            player.health_point = 0
                            self.die_order.append(player.number)
                            self.die_list.append(player.number)
                            player.change_status(character.Character.REAL_DEAD)
                            self.print_debug(7, 'player', player.number, 'dead out of circle')
                    if player.health_point > player.health_point_limit:
                        player.health_point = player.health_point_limit
            pass

        def items():
            pass

        def noise():
            for _sound in self.all_sounds:
                assert isinstance(_sound, sound.Sound)
                _sound.update()
                if _sound.arrived():
                    pos = character.Character.all_characters[_sound.receiver].position
                    self.all_info[_sound.receiver].sounds.append((_sound.emitter, _sound.delay, _sound.get_data(pos)))
            self.all_sounds = [_sound for _sound in self.all_sounds if not _sound.arrived()]
            return

        def update():

            for team in self.all_players:
                for player in team:
                    if player.move_cd:
                        player.move_cd -= 1
                    if player.shoot_cd:
                        player.shoot_cd -= 1
                    if player.is_picking():
                        player.change_status(character.Character.RELAX)
                    if player.move_cd == 0:

                        if player.is_flying():
                            # this is change from flying to jumping
                            player.status = character.Character.JUMPING
                            player.position = player.jump_position
                            try:
                                player.move_direction = (player.land_position - player.jump_position).unitize()
                            except ZeroDivisionError:
                                player.move_direction.x = player.move_direction.y
                                player.move_direction.y = -player.move_direction.x
                            player.move_speed = character.Character.JUMPING_SPEED
                            player.move_cd = int((player.land_position - player.jump_position).length() /
                                                 player.move_speed + 1)
                            player.face_direction = player.move_direction
                        elif player.is_jumping():
                            # jump to the land, and then relax
                            player.status = character.Character.RELAX
                            player.position = player.land_position
                            player.move_direction = None
                            player.move_speed = 0
                            self.print_debug(8, "in turn", self.__turn, "player", player.number, "reach the ground at",
                                             player.position)

            class RelativeObject:
                def __init__(self, _player, target):
                    self.target = target
                    self.player = _player
                    self.distance, self.angle = _player.position.get_polar_position(_player.face_direction,
                                                                                    target.position)
                    self.angle = 360 - self.angle if self.angle > 180 else self.angle

            for player_id, player_info in self.all_info.items():
                # sounds information have been processed in noise()
                player = character.Character.all_characters[player_id]
                if player.is_flying():
                    continue

                # here deal with terrain and other player's information
                targets = []
                other_set = set()
                landform_set = set()
                for team in self.all_players:
                    for other in team:
                        if other.number == player_id:
                            continue
                        targets.append(RelativeObject(player, other))

                for key, block in self.map.all_blocks.items():
                    targets.append(RelativeObject(player, block))
                targets = [target for target in targets if
                           0 < target.distance < player.view_distance * 1.1 and target.angle <= player.view_angle / 2]
                targets.sort(key=lambda target: target.distance)
                angle = player.face_direction.get_angle()
                theta = - player.view_angle / 2
                delta = player.view_angle / 120

                while theta <= player.view_angle / 2:
                    start = player.position
                    over = start + position.angle_to_position(angle + theta) * player.view_distance
                    for target in targets:
                        if target.target.is_intersecting(start, over):
                            if isinstance(target.target, character.Character):
                                other_set.add(target.target)
                            else:
                                landform_set.add(target.target)
                            # if it's opaque, this view line is end
                            if target.target.is_opaque():
                                break
                    theta += delta

                # check other players manually
                targets = [target.target for target in targets if isinstance(target.target, character.Character)]
                targets = list(set(targets).difference(set(other_set)))
                for other in targets:
                    if self.map.accessible(player.position, other.position):
                        other_set.add(other)

                # modify player information
                player_info.others = [target.number for target in other_set]
                player_info.landform = [target.id for target in landform_set]
                self.print_debug(20, 'player', player.number, 'vision list for others:', player_info.others)
                self.print_debug(25, 'player', player.number, 'vision list for landform:', player_info.landform)

                # deal with player's vision for items
                for item_id in self.all_wild_items:
                    each_item = item.Item.all_items[item_id]
                    distance, angle = player.position.get_polar_position(player.face_direction, each_item.position)
                    if distance <= player.view_distance and abs(angle) <= player.view_angle / 2:
                        player_info.items.append(item_id)
                self.print_debug(21, 'player', player_id, 'see item', player_info.items)

            if self.poison.update():
                self.print_debug(17, "the circle's center:", self.poison.center_now, 'radius:', self.poison.radius_now)
            return

        def pack_for_interface():
            data = interface.FrameInfo()
            # give frame
            data.frame = self.__turn
            # give information for each player
            for team in self.all_players:
                for player in team:
                    if player.is_flying() or not player.is_alive():
                        continue
                    elif player.is_jumping():
                        # give parachute information
                        new_info = data.parachutists.add()
                        new_info.id = player.number
                        new_info.HP = int(player.health_point)
                        new_info.face_direction = player.face_direction.get_angle()
                        new_info.pos.x, new_info.pos.y = player.position.x, player.position.y
                        new_info.jump_pos.x, new_info.jump_pos.y = player.jump_position.x, player.jump_position.y
                        new_info.land_pos.x, new_info.land_pos.y = player.land_position.x, player.land_position.y
                    else:
                        # give normal player information
                        new_info = data.players.add()
                        new_info.id = player.number
                        new_info.HP = int(player.health_point)
                        new_info.pos.x, new_info.pos.y = player.position.x, player.position.y
                        new_info.weapon = player.last_weapon
                        new_info.armor = player.best_armor
                        new_info.face_direction = player.face_direction.get_angle()
            # give all items information
            for item_id, type_pos_tuple in self.all_wild_items.items():
                type_id, pos = type_pos_tuple
                new_item = data.items.add()
                new_item.id = item_id
                new_item.type = type_id
                new_item.pos.x, new_item.pos.y = pos.x, pos.y

            # give circle's information
            data.circle.status = self.poison.flag
            data.circle.frames = self.poison.rest_frames
            if self.poison.is_processing():
                data.circle.now.center.x, data.circle.now.center.y = self.poison.center_now.x, self.poison.center_now.y
                data.circle.next.center.x, data.circle.next.center.y = \
                    self.poison.center_next.x, self.poison.center_next.y
                data.circle.now.radius = self.poison.radius_now
                data.circle.next.radius = self.poison.radius_next
            return data

        self.print_debug(10, 'turn', self.__turn, 'starts!')

        # 1. judge and operate players' instructions
        instructions()

        # 2. all players move
        move()

        # 3. all bullets and shells fly on
        attack()

        # 4. calculate all damage(including healing)
        damage()

        # 5. judge if one dies
        die()

        # 6. refresh items information
        items()

        # 7. refresh radio and other sound
        noise()

        # 8. update player's view, cd and etc
        update()

        self.__turn = self.__turn + 1

        # output data for playback file
        self.write_playback(pack_for_interface())

        # return pack data after refreshing
        return self.pack_for_platform()

    # here return everything as i mention in the related files
    def pack_for_platform(self):
        all_data = {}
        for number, player_info in self.all_info.items():
            player = character.Character.all_characters[number]
            if not isinstance(player, character.Character):
                raise Exception("wrong type of player!")
            data = platform.PlayerInfo()
            data.player_ID = player.number
            data.self.health_point = player.health_point
            data.self.health_point_limit = player_info.hp_max
            data.self.move_angle = player.move_direction.get_angle() if player.move_direction else 0
            data.self.view_angle = player.face_direction.get_angle()
            data.self.move_speed = player.move_speed
            data.self.status = player.status
            data.self.move_cd = player.move_cd
            data.self.attack_cd = player.shoot_cd
            data.self.pos.x, data.self.pos.y = player.position.x, player.position.y

            # player's bag information
            for item_id in player.bag:
                new_item = data.self.bag.add()
                entity = item.Item.all_items[item_id]
                new_item.item_ID = item_id
                new_item.type = entity.item_type
                new_item.durability = entity.durability

            # player's vision for landform
            data.landform_id.extend(player_info.landform)

            # player's vision for items
            for item_id in player_info.items:
                new_item = data.items.add()
                entity = item.Item.all_items[item_id]
                new_item.item_ID = item_id
                new_item.type = entity.item_type
                new_item.durability = entity.durability
                new_item.pos.distance, new_item.pos.angle = \
                    player.position.get_polar_position(player.face_direction, entity.position)

            # player's vision for other players
            for player_id in player_info.others:
                new_other = data.others.add()
                other = character.Character.all_characters[player_id]
                if not isinstance(other, character.Character):
                    raise Exception("wrong type of player!")
                new_other.player_ID = player_id
                new_other.status = other.status
                new_other.move_angle = other.move_direction.get_angle() if other.move_direction else 0
                new_other.view_angle = other.face_direction.get_angle()
                new_other.move_speed = other.move_speed
                new_other.vocation = other.vocation
                new_other.pos.distance, new_other.pos.angle = \
                    player.position.get_polar_position(player.face_direction, other.position)

            # player's audition
            for arrived_sound in player_info.sounds:
                new_sound = data.sounds.add()
                new_sound.sender, new_sound.delay, new_sound.parameter = arrived_sound

            # the circle's information
            data.poison.move_flag = self.poison.flag
            data.poison.rest_frames = self.poison.rest_frames
            if self.poison.is_processing():
                data.poison.current_center.x = self.poison.center_now.x
                data.poison.current_center.y = self.poison.center_now.y
                data.poison.next_center.x = self.poison.center_next.x
                data.poison.next_center.y = self.poison.center_next.y
                data.poison.current_radius = self.poison.radius_now
                data.poison.next_radius = self.poison.radius_next

            proto_data = data.SerializeToString()
            all_data[number] = proto_data
        all_data['dead'] = self.die_list
        self.print_debug(50, "return", len(all_data), "players' data back to platform")
        return all_data

    def write_playback(self, interface_data):
        data = interface_data.SerializeToString()
        with open(self.playback_file_path, 'ab') as playback:
            playback.write(struct.pack('i', len(data)))
            playback.write(data)
        self.print_debug(50, "write", len(data), "bytes into the playback file")
        return

    def anti_infinite_loop(self):
        # the game can hold no more than half an hour
        # later, we will design poison circle, but now I can just use enforcement measure
        return self.__turn < 2 * 60 * 25

    def print_debug(self, level, *args, sep=' ', end='\n', file=None):
        # print debug log if current debug level is higher than message debug level
        if self.__debug_level >= level:
            print(*args, sep=sep, end=end, file=file)


if __name__ == '__main__':
    # if necessary, test here
    pass
