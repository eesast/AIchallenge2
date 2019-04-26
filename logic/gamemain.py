#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass import *
import proto.interface_pb2 as interface
import proto.platform_pb2 as platform
# from multiprocessing import Pool
from random import randrange
from random import random
from json import load
from json import dump
import math
import time
import struct

#   here define a debug level variable to debug print-oriented
#   remember: here is just a initial level for logic
#   platform may give another number in game_init
PRINT_DEBUG = 26


#   !!set PRINT_DEBUG to -1 to close the debug system!!


#   level 0: print key stage information for the game
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
#   level 18: print player's scope information
#   level 19: print player's illegal param for instructions

#   level 23: print player's view for other players
#   level 24: print player's view for items
#   level 25: print player's view for landforms
#   level 26: print player's missing shooting
#   level 27: print player's sounds list

#   level 29: print all non-redundant commands for each frame
#   level 30: print all commands for each frame

#   level 40: print player's moving over information

#   level 50: print data length for proto

#   level 100: will give all information you can imagine, including config file


class GameMain:
    # if not specified, platform needn't this class's members
    map_size = 1000

    def __init__(self):

        # it's more like a define instead of an initialization
        self.die_order = []  # save the player's dying order and frames
        self.die_list = []  # die order in this frame for platform
        self.map_items = [[set() for row in range(10)] for column in range(10)]  # try to divide map into 256 parts
        self.map = terrain.Map()
        self.last_alive_teams = []

        self.all_players = []  # save all teams and players
        self.all_bullets = []
        self.all_sounds = []
        self.all_drugs = []
        self.new_items = []
        self.removed_items = []
        self.all_parameters = {}
        self.all_areas_players = {}
        self.all_kills = {}
        self.all_info = {}  # save all information for platform
        self.all_commands = {"move": {}, "shoot": {}, "pickup": {}, "radio": {}}
        self.all_visions = {}

        self.number_to_team = {}  # use a number to find a team
        self.number_to_player = {}  # use a number to find a player
        self.__start_position, self.__over_position = None, None
        self.__turn = 0
        self.poison = None
        self.last_poison_flag = None
        self.pool = None

        # initialize debug level for logic to use directly and for platform to change it
        self.__debug_level = PRINT_DEBUG

        # for error ai
        self.no_input_player_list = []

        # for playback file
        self.playback_file = None

        self.print_debug(0, 'GameMain initialize finished')

        return

    def set_debug_level(self, level):
        if level is not None:
            self.__debug_level = level
        return

    def load_data(self, file_path, file_name):
        def load_parameter(parent_path, parameter_file_path):
            with open(parent_path + parameter_file_path, "r", encoding="utf-8") as file:
                parameter_data = load(file)
            self.all_parameters = parameter_data['main']
            character.Character.all_params = parameter_data['character']
            character.Character.JUMPING_SPEED = parameter_data['character']['jumping']
            character.Character.AIRPLANE_SPEED = parameter_data['character']['airplane']
            return parameter_data

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
        self.playback_file = open(file_path + playback_child_path, 'wb')

        # for circle data
        self.print_debug(100, self.poison.load_data(file_path, global_config["CIRCLE_FILE_PATH"]))

        # for parameters
        self.print_debug(100, load_parameter(file_path, global_config["PARAMETER_FILE_PATH"]))

        self.print_debug(0, 'all data load finished')
        return

    def map_init(self):
        # here should give some items randomly according to occurrence
        for i in range(self.poison.all_data[0]['items']):
            # get drop position
            area_id = self.map.get_random_area_id()
            area = self.map.areas[area_id]
            block = area.airdrop_blocks[randrange(0, len(area.airdrop_blocks))]
            pos = block.get_random_position()
            # print(pos.get_area_id(), area_id)
            # assert pos.get_area_id() == area_id
            # add item
            item_type = item.Item.get_random_item()
            new_id = item.Item.add(item_type, pos)
            new_item = item.Item.all_items[new_id]
            self.new_items.append(new_item)
            self.map_items[area_id // 10][area_id % 10].add(new_item)
        self.print_debug(0, 'map items initialize finished')
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
                    self.all_commands["move"][playerID] = command["move_angle"], command["view_angle"], command['other']
                elif command_type == character.SHOOT:
                    self.all_commands["shoot"][playerID] = \
                        command["view_angle"], command["target"], command["other"]
                elif command_type == character.PICKUP:
                    self.all_commands["pickup"][playerID] = command["target"], command["other"]
                elif command_type == character.RADIO:
                    if not self.all_commands["radio"].get(playerID, None):
                        self.all_commands["radio"][playerID] = []
                    self.all_commands["radio"][playerID].append((command["target"], command["other"]))
                else:
                    # if command_type isn't correct, it will be ignored
                    continue
        self.print_debug(29, "unwrap_command successfully")
        self.print_debug(29, self.all_commands)
        return

    def __load_map(self, parent_path, map_file_path):
        self.map.initialize(terrain.Area.load_data(parent_path, map_file_path))
        vision.Sweep.areas = self.map.areas
        self.map_size = GameMain.map_size
        self.poison = circle.Circle(self.map_size)
        return

    def alive_teams(self):
        teams = []
        for team in self.last_alive_teams:
            alive_flag = False
            alive = []
            for player in team:
                # judge if there is an alive player still standing
                if player.health_point > 0:
                    alive_flag = True
                # add player not real dead
                if player.is_alive():
                    alive.append(player)
            # if there is player not real dead
            if len(alive):
                # judge if there is any player standing in this team
                if alive_flag:
                    teams.append(alive)
                else:
                    # or the whole team should be out
                    for player in alive:
                        player.change_status(character.Character.REAL_DEAD)
                        self.die_order.append((player.number, self.__turn))
                        self.die_list.append(player.number)
                        self.all_kills.setdefault(player.killer, []).append(player.number)
                        self.print_debug(7, 'player', player.number, 'died because of team wipe')
        self.last_alive_teams = teams
        return teams

    def game_over(self):
        return len(self.alive_teams()) <= 1

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

                if new_vocation == character.Character.NO_VOCATION:
                    self.print_debug(0, 'player', player_number, 'gives nothing or negative vocation')
                    self.no_input_player_list.append(player_number)

                # first judge if this vocation is legal
                if not 0 <= new_vocation < character.Character.VOCATION_COUNT:
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
            self.last_alive_teams = self.all_players
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
                # first we must make sure player won't jump into the sea, so I adjust directly for them
                while self.map.areas[player.land_position.get_area_id()].name == 'sea':
                    self.print_debug(1, 'player', player.number, "'s jump position", player.land_position, end='')
                    player.land_position.x += 100 if player.land_position.x < 500 else -100
                    player.land_position.y += 100 if player.land_position.y < 500 else -100
                    self.print_debug(2, 'is adjust to', player.land_position)

                player.jump_position = get_pedal(player.land_position, player.number)
                player.move_direction = (self.__over_position - self.__start_position).unitize()
                player.position = self.__start_position
                player.move_speed = character.Character.AIRPLANE_SPEED
                player.move_cd = int((player.jump_position - self.__start_position).length() / player.move_speed + 1)
                player.face_direction = player.move_direction
                player.status = character.Character.ON_PLANE
                # meanwhile deal with information dictionary
                self.all_info[player.number] = info.Information(player)
                self.all_visions[player.number] = None

        # output data for interface
        self.write_playback(get_proto_data())

        # now everything down, main operation starts
        # return first turn's information
        return self.refresh()

    def refresh(self):  # refresh a new frame according to the orders

        def instructions():
            self.removed_items.clear()
            self.all_bullets.clear()
            self.all_drugs.clear()
            # pick up
            for player_number, command in self.all_commands['pickup'].items():
                picked_item = item.Item.all_items.get(command[0], None)
                player = self.number_to_player[player_number]
                if picked_item is None:
                    self.print_debug(4, 'player', player_number, 'try to pick item not existing or belonging to others')
                elif picked_item.number not in self.all_info[player_number].items:
                    self.print_debug(4, 'player', player_number, 'try to pick item out of view')
                elif not player.pick_accessible(picked_item.position):
                    self.print_debug(4, 'player', player_number, "try to pick item beyond pick range")
                else:
                    if picked_item.data.get('mode', None) == 'TRIGGERED':
                        if picked_item.data['macro'] == 'CODE_CASE':
                            if player.vocation == character.Character.HACK:
                                item.Item.remove(picked_item.number)
                                area_id = picked_item.position.get_area_id()
                                self.removed_items.append(command[0])
                                self.map_items[area_id // 10][area_id % 10].remove(picked_item)
                                self.print_debug(16, 'player', player_number, 'opens code case', picked_item.number,
                                                 end='')
                                # now open the case
                                new_item = item.Item.get_reward_item()
                                data = item.Item.all_data[new_item]
                                durability = data['durability']
                                player.bag[new_item] = player.bag.get(new_item, 0) + durability
                                self.number_to_player[player_number].change_status(character.Character.PICKING)
                                self.print_debug(16, 'and he gets a', data['name'])
                            else:
                                self.print_debug(4, 'player', player_number, "try to open code case but isn't a hack")
                        else:
                            # currently i just design only one triggered item: code case
                            pass
                    else:
                        # now this player can get it
                        area_id = picked_item.position.get_area_id()
                        try:
                            self.map_items[area_id // 10][area_id % 10].remove(picked_item)
                        except KeyError:
                            print('when you see this message, please contact with logic group with log below')
                            found = False
                            for i in range(10):
                                for j in range(10):
                                    if picked_item in self.map_items[i][j]:
                                        print('item in the area', i, j, 'but area id is', area_id)
                                        found = True
                                        break
                                if found:
                                    break
                            if not found:
                                print('item', picked_item.number, 'not in the map, maybe has been picked')
                                continue

                        player.bag[picked_item.item_type] = player.bag.get(picked_item.item_type,
                                                                           0) + picked_item.durability
                        item.Item.remove(picked_item.number)
                        self.removed_items.append(command[0])
                        self.number_to_player[player_number].change_status(character.Character.PICKING)
                        self.print_debug(16, 'player', player_number, 'picks', picked_item.data['name'],
                                         picked_item.number)
                        # maybe we should deal with command['other'], now ignore it

            # move
            for player_id, command in self.all_commands['move'].items():
                move_angle, view_angle, real_move = command
                player = self.number_to_player[player_id]
                if not player.command_status_legal(character.MOVE):
                    self.print_debug(5, 'player', player_id, 'try to move but not in right status')
                elif not 0 <= view_angle <= 360:
                    self.print_debug(3, 'player', player_id, 'give wrong view angle as', view_angle)
                elif not real_move:
                    old_angle = player.face_direction.get_angle()
                    player.face_direction = position.angle_to_position(view_angle + old_angle)
                    self.print_debug(15, 'player', player_id, 'adjust view angle to', old_angle + view_angle)
                elif not 0 <= move_angle <= 360:
                    self.print_debug(3, 'player', player_id, 'give wrong move angle as', move_angle)
                else:  # now do it
                    player.change_status(character.Character.MOVING)
                    basic_angle = player.face_direction.get_angle()
                    player.face_direction = position.angle_to_position(view_angle + basic_angle)
                    player.move_direction = position.angle_to_position(move_angle + basic_angle)
            # shoot
            for player_id, command in self.all_commands['shoot'].items():
                view_angle, item_type, other = command
                player = self.number_to_player[player_id]
                rest = player.bag.get(item_type, 0)
                item_data = item.Item.all_data.get(item_type, None)
                if item_data is None:
                    self.print_debug(3, 'player', player_id, 'try to shoot with not existing item', item_type)
                elif not player.command_status_legal(character.SHOOT):
                    self.print_debug(5, 'player', player_id, 'try to shoot but not in right status')
                elif player.shoot_cd:
                    self.print_debug(4, 'player', player_id, 'try to shoot with', player.shoot_cd, ' shoot cd')
                elif item_type == -1:
                    # abandon current scope
                    player.equip_scope(1)
                    self.print_debug(18, 'player', player_id, "abandoned current scope(if he's wearing one)")
                    if 0 <= view_angle <= 360:
                        player.face_direction = position.angle_to_position(
                            player.face_direction.get_angle() + view_angle)
                elif not rest:
                    self.print_debug(4, 'player', player_id, 'try to use weapon without durability')
                elif item_data['type'] != 'WEAPON' and item_data['mode'] != 'SPENDABLE':
                    self.print_debug(4, 'player', player_id, 'try to use not weapon-like item to shoot')
                elif item_data['param'] < 0:
                    if player.vocation == character.Character.MEDIC and other >= 0:
                        if other in self.number_to_team[player.team]:
                            if self.number_to_player[other].pick_accessible(player.position):
                                if self.number_to_player[other].can_be_healed():
                                    self.all_drugs.append((item_type, other, player_id))
                                    player.bag[item_type] -= 1
                                    player.shoot_cd = item_data['cd']
                                    player.last_weapon = item_type
                                    player.change_status(character.Character.SHOOTING)
                                else:
                                    self.print_debug(19, 'player', player_id, 'try to use drug to dead player', other)
                            else:
                                self.print_debug(19, 'player', player_id, 'try to use drug beyond range')
                        else:
                            self.print_debug(19, 'player', player_id, 'try to use drug to player not in the same team')
                    else:
                        player.bag[item_type] -= 1
                        self.all_drugs.append((item_type, player_id, None))
                        player.shoot_cd = item_data['cd']
                        player.last_weapon = item_type
                        player.change_status(character.Character.SHOOTING)
                elif 'SCOPE' in item_data['macro']:
                    player.equip_scope(int(item_data['param']))
                    player.bag[item_type] -= 1
                    player.shoot_cd = item_data['cd']
                    self.print_debug(18, 'player', player_id, 'equip', item_data['macro'])
                    if 0 <= view_angle <= 360:
                        player.face_direction = position.angle_to_position(
                            player.face_direction.get_angle() + view_angle)
                elif not 0 <= view_angle <= 360:
                    self.print_debug(3, 'player', player_id, 'give wrong attack angle as', view_angle)
                else:  # now shoot
                    player.bag[item_type] -= 1
                    view_angle += player.face_direction.get_angle()  # correct relative angle to absolute angle
                    player.shoot_cd = item_data['cd']
                    player.face_direction = position.angle_to_position(view_angle)
                    player.change_status(character.Character.SHOOTING)
                    self.all_bullets.append((player.position, view_angle, item_type, player_id, None))
                    player.last_weapon = item_type
                    # here should deal with other parameter, just put off

                    # here deal with gun sound
                    for _team in self.all_players:
                        muffler = item.Item.all_data['MUFFLER']
                        factor = muffler['param'] if player.bag.get(muffler['number']) else 1
                        for receiver in _team:
                            if receiver is player:
                                continue
                            if abs(receiver.position - player.position) < factor * sound.Sound.farthest['gun']:
                                self.all_sounds.append(sound.Sound(sound.Sound.GUN_SOUND, receiver.number,
                                                                   player.position,
                                                                   abs(player.position - receiver.position)))
            # radio
            for emitter_id, commands in self.all_commands['radio'].items():
                # here receiver_id include some other data for signalman, awaiting to process
                emitter = self.number_to_player[emitter_id]
                if emitter.vocation != character.Character.SIGNALMAN:
                    # if he isn't signal man, only last instruction will be processed
                    commands = commands[-1:]
                else:
                    commands = commands[-int(character.Character.all_data[emitter.vocation]['skill']):]
                for receiver_id, data in commands:
                    receiver = self.number_to_player.get(receiver_id)
                    if not receiver:
                        self.print_debug(4, emitter, 'try to send radio to player not existing')
                    elif receiver.team != emitter.team:
                        self.print_debug(4, emitter, 'try to send radio to other team')
                    elif receiver is emitter:
                        self.print_debug(4, emitter, 'try to send radio to himself')
                    else:
                        self.all_sounds.append(sound.Sound(sound.Sound.RADIO_VOICE, receiver_id, emitter.position, abs(
                            emitter.position - receiver.posistion), emitter_id, data))
            return

        def move():
            self.all_areas_players.clear()
            for team in self.all_players:
                for player in team:
                    self.all_info[player.number].clear()
                    past_position = player.position
                    if player.update():
                        if player.is_flying() or player.is_jumping() or self.map.stand_permitted(player.position,
                                                                                                 player.radius):
                            self.print_debug(15, 'player', player.number, 'move to', player.position)
                            # check if player is standing on a block such as grass
                            for block in self.map.areas[player.position.get_area_id()].blocks:
                                if block.name == 'shallow_water' and player in block:
                                    player.block = block
                                    break
                                elif 'grass' in block.name and player in block:
                                    player.block = block
                                    break
                            else:
                                player.block = None

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
                    self.all_areas_players.setdefault(player.position.get_area_id(), []).append(player)

        def items():
            self.new_items.clear()
            if self.last_poison_flag is None:
                # initialize items in the map
                self.map_init()
            elif self.poison.flag == 1 and self.last_poison_flag == 2:
                # generate items when the circle start to shrink in each stage
                for i in range(0, self.poison.all_data[self.poison.stage]['items'], 25):
                    # get drop position
                    area_id = self.map.get_random_area_id()
                    area = self.map.areas[area_id]
                    for j in range(5):
                        block = area.airdrop_blocks[randrange(0, len(area.airdrop_blocks))]
                        for k in range(5):
                            pos = block.get_random_position()
                            # add item
                            item_type = item.Item.get_random_item()
                            new_id = item.Item.add(item_type, pos)
                            new_item = item.Item.all_items[new_id]
                            self.new_items.append(new_item)
                            self.map_items[area_id // 10][area_id % 10].add(new_item)
                self.print_debug(0, 'items added finished in turn', self.__turn)
            self.last_poison_flag = self.poison.flag
            return

        def attack():
            def update_vision(player_id):
                # deal with vision
                player = self.number_to_player[player_id]
                player_info = self.all_info[player_id]
                if player.is_flying():
                    return

                new_vision = vision.Sweep(player, self.all_areas_players, self.map_items)
                self.all_visions[player_id] = new_vision
                for block in new_vision.get_visible_targets():
                    if isinstance(block, character.Character):
                        player_info.others.append(block.number)
                    elif isinstance(block, item.Item):
                        player_info.items.append(block.number)
                    else:
                        player_info.landform.append(block.number)

                # print player information
                self.print_debug(23, 'player', player.number, 'vision list for others:', player_info.others)
                self.print_debug(24, 'player', player.number, 'vision list for items:', player_info.items)
                self.print_debug(25, 'player', player.number, 'vision list for landform:', player_info.landform)
                return

            def update_bullets():
                bullets = self.all_bullets
                for index in range(len(bullets)):
                    pos, view_angle, item_type, player_id, hit_id = bullets[index]
                    shortest = None
                    data = item.Item.all_data[item_type]
                    team_id = self.number_to_player[player_id].team
                    for target_id in self.all_info[player_id].others:
                        player = self.number_to_player[target_id]
                        # teammate and no hp player will be ignored
                        if player.team == team_id or not player.can_be_hit():
                            continue
                        # player in water has 30 percent probability to miss the bullet
                        if player.block and player.block.name == 'shallow_water' and random() < 0.3:
                            continue
                        dist2, delta = pos.get_polar_position2(position.angle_to_position(view_angle), player.position)
                        delta = 0 if delta > 360 else 360 - delta if delta > 180 else delta
                        if delta < data['param'] / 2:
                            if dist2 > data['range'] * data['range']:
                                continue
                            if shortest is None or shortest < dist2:
                                # modify hit player
                                shortest = dist2
                                bullets[index] = pos, view_angle, item_type, player_id, player.number

                return

            def vision_extra_process(player_id):
                def available(target):
                    other_player = self.number_to_player[target]
                    if other_player.block and 'grass' in other_player.block.name:
                        return player.block is other_player.block
                    return True

                # here deal with grass
                player = self.number_to_player[player_id]
                player_info = self.all_info[player_id]
                player_info.others = [other for other in player_info.others if available(other)]

                return

            # update vision first
            for player_number in self.all_info:
                update_vision(player_number)
            # then deal with bullets
            update_bullets()
            # deal with vision for special condition
            for player_number in self.all_info:
                vision_extra_process(player_number)
            return

        def damage():
            bullets = self.all_bullets
            for index in range(len(bullets)):
                pos, view_angle, item_index, player_id, hit_id = bullets[index]
                if hit_id is not None:
                    shooter = self.number_to_player[player_id]
                    direction = position.angle_to_position(view_angle)
                    target = shooter.position
                    dist = abs(position.cross_product(direction, target - pos))
                    data = item.Item.all_data[item_index]
                    value = math.exp(- dist * self.all_parameters['damage_param'] / data['range']) ** 2 * data['damage']
                    if shooter.vocation == character.Character.SNIPER and 'SNIPER' in data['name']:
                        value *= character.Character.all_data[character.Character.SNIPER]['skill']
                    parameter = 'ARMOR_PIERCING' if data['name'] == 'CROSSBOW' else None
                    real_damage = self.number_to_player[hit_id].get_damage(value, player_id, parameter)
                    shooter.fire = hit_id, item_index
                    self.print_debug(13, 'player', player_id, data['name'], real_damage, 'damage to player', hit_id)
                else:
                    shooter = self.number_to_player[player_id]
                    shooter.fire = -1, item_index
                    self.print_debug(26, 'player', player_id, 'shoot at nothing')

            for drug_index, receiver, emitter in self.all_drugs:
                drug = item.Item.all_data[drug_index]
                value = drug['param']
                if emitter is None:
                    self.number_to_player[receiver].get_damage(value)
                    self.print_debug(13, 'player', receiver, drug['name'], value, 'heal points to himself')
                else:
                    value *= character.Character.all_data[character.Character.MEDIC]['skill']
                    self.number_to_player[receiver].get_damage(value)
                    self.print_debug(13, 'player', emitter, drug['name'], value, 'head points to player', receiver)

            return

        def die():
            self.die_list.clear()
            if not self.__turn:
                for player_id in self.no_input_player_list:
                    player = self.number_to_player[player_id]
                    player.health_point = 0
                    self.all_kills.setdefault(player.killer, []).append(player.number)
                    self.die_order.append((player.number, self.__turn))
                    player.change_status(character.Character.REAL_DEAD)
                    self.print_debug(7, 'player', player.number, 'died because of nothing input')
            for team in self.all_players:
                for player in team:
                    if not player.can_be_healed():
                        # skip real dead player
                        continue
                    if self.poison.safe(player):
                        if player.can_be_hit():
                            if player.health_point <= 0:
                                player.health_point = 0
                                player.change_status(character.Character.DEAD)
                                self.print_debug(7, 'player', player.number, 'died')
                        elif player.health_point > 0:
                            player.change_status(character.Character.RELAX)
                            player.killer = -1
                            self.print_debug(7, 'player', player.number, 'resurrected')
                    else:
                        # to understand this part of code, i will give explain how the player.killer works:
                        # if some player hit this player in poison in one frame, the one who gives him most damage
                        # will surely be the killer
                        # if some body kill this player in safe area, frames latter the circle shrink to here,
                        # then though the player.most_damage is 0, but player.killer is still the murder
                        # if this player is alive but get poison to die with some other damage in the same frame, then
                        # if somebody give him more damage than circle, killer will be him, or killer is -1
                        # if this poor gay
                        if player.get_damage(self.poison.damage_per_frame, -1, 'ARMOR_PIERCING'):
                            self.print_debug(13, 'the circle', self.poison.damage_per_frame, 'damage to', player.number)
                        if player.health_point <= 0:
                            player.health_point = 0
                            self.all_kills.setdefault(player.killer, []).append(player.number)
                            self.die_order.append((player.number, self.__turn))
                            self.die_list.append(player.number)
                            player.change_status(character.Character.REAL_DEAD)
                            self.print_debug(7, 'player', player.number, 'died out of circle')
                    if player.health_point > player.health_point_limit:
                        player.health_point = player.health_point_limit

        def noise():
            for _sound in self.all_sounds:
                assert isinstance(_sound, sound.Sound)
                _sound.update()
                if _sound.arrived():
                    pos = self.number_to_player[_sound.receiver].position
                    self.all_info[_sound.receiver].sounds.append((_sound.emitter, _sound.delay, _sound.get_data(pos)))
            self.all_sounds = [_sound for _sound in self.all_sounds if not _sound.arrived()]
            for player_id, player_info in self.all_info.items():
                self.print_debug(27, "player", player_id, "'s sounds list:", player_info.sounds)
            return

        def update():
            def update_for_each(player_number):
                player = self.number_to_player[player_number]
                # deal with status
                if not player.can_be_hit():
                    return

                if player.is_picking():
                    player.change_status(character.Character.RELAX)

                if player.shoot_cd:
                    player.shoot_cd -= 1
                    if player.shoot_cd == 0:
                        player.change_status(character.Character.RELAX)

                if player.move_cd:
                    player.move_cd -= 1
                if player.move_cd == 0:

                    if player.is_flying():
                        # this is change from flying to jumping
                        player.status = character.Character.JUMPING
                        player.position = player.jump_position
                        player.move_direction = (player.land_position - player.jump_position).unitize()
                        player.move_speed = character.Character.JUMPING_SPEED
                        player.move_cd_max = int((player.land_position - player.jump_position).length() /
                                                 player.move_speed + 1)
                        player.move_cd = player.move_cd_max
                        player.face_direction = player.move_direction
                        self.print_debug(8, "player", player.number, "leave the plane at", player.position)
                    elif player.is_jumping():
                        # jump to the land, and then relax
                        player.status = character.Character.RELAX
                        player.position = player.land_position
                        while not self.map.stand_permitted(player.position, player.radius):
                            # here we should adjust player's position
                            block = self.map.last_bumped_block
                            vector = player.position - block.position
                            direction = vector.unitize()
                            if block.shape == object.Object.CIRCLE:
                                adjust_distance = player.radius + block.radius - abs(vector)
                                new_position = player.position + direction * adjust_distance
                            else:
                                distance = abs(vector) + block.radius / 10
                                new_position = player.position
                                while block.is_bumped(new_position, player.radius):
                                    distance += block.radius / 10
                                    new_position = player.position + direction * distance
                            print('player', player.number, 'from', player.position, "adjusted to", new_position)
                            player.position = new_position
                        player.move_direction = None
                        player.move_speed = 0
                        self.print_debug(8, "in turn", self.__turn, "player", player.number, "reach the ground at",
                                         player.position)
                    else:
                        player.change_status(character.Character.RELAX)
                        player.move_direction = None
                        player.move_speed = 0
                        self.print_debug(40, 'player', player.number, 'move over')

            for player_id in self.all_info:
                update_for_each(player_id)
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
                    if player.is_flying():
                        continue
                    else:
                        # give normal player information
                        new_info = data.players.add()
                        new_info.id = player.number
                        if not player.is_alive():
                            new_info.real_dead = True
                            continue
                        new_info.HP = int(player.health_point)
                        new_info.pos.x, new_info.pos.y = player.position.x, player.position.y
                        new_info.weapon = player.last_weapon
                        new_info.armor = player.best_armor
                        new_info.face_direction = player.face_direction.get_angle()
                        new_info.height = float(player.get_height())
                        if player.fire:
                            new_info.fire_info.fire = True
                            new_info.fire_info.target, new_info.fire_info.weapon = player.fire
                            player.fire = None

            # give all new items information
            for each_item in self.new_items:
                pos = each_item.position
                new_item = data.new_items.add()
                new_item.id = each_item.number
                new_item.type = each_item.item_type
                new_item.pos.x, new_item.pos.y = pos.x, pos.y

            # give all removed items information
            data.removed_items.extend(self.removed_items)

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

        # output data for playback file
        self.write_playback(pack_for_interface())

        self.__turn += 1

        # deal with last frame
        if self.game_over():
            self.over_process()

        # return pack data after refreshing
        return self.pack_for_platform()

    # here return everything as i mention in the related files
    def pack_for_platform(self):
        all_data = {}
        for number, player_info in self.all_info.items():
            player = self.number_to_player[number]

            data = platform.PlayerInfo()
            data.player_ID = player.number

            data.self.health_point = player.health_point
            data.self.health_point_limit = player_info.hp_max
            data.self.move_angle = player.move_direction.get_angle() if player.move_direction else 0
            data.self.view_angle = player.face_direction.get_angle()
            data.self.move_speed = player.move_speed
            data.self.vocation = player.vocation
            data.self.status = player.status
            data.self.move_cd = player.move_cd
            data.self.attack_cd = player.shoot_cd
            data.self.pos.x, data.self.pos.y = player.position.x, player.position.y
            data.self.vocation = player.vocation
            data.self.view_width = player.view_angle
            data.self.view_distance = player.view_distance

            # player's bag information
            for item_type in player.bag:
                new_item = data.self.bag.add()
                new_item.type = item_type
                new_item.durability = int(player.bag[item_type])

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
                other = self.number_to_player[player_id]
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
        if self.playback_file.closed:
            return
        data = interface_data.SerializeToString()
        self.playback_file.write(struct.pack('i', len(data)))
        self.playback_file.write(data)
        self.playback_file.flush()
        self.print_debug(50, "write", len(data), "bytes into the playback file")
        return

    def over_process(self):
        # deal with the winner
        win_team = [player.number for player in (self.last_alive_teams[0] if len(self.last_alive_teams) else [])]
        self.print_debug(0, 'in turn', self.__turn, 'game over with alive teams:', win_team)
        for player in win_team:
            self.die_list.append(player)

        # deal with the score
        score = {}
        team_save = {}
        for team in self.all_players:
            team_save[team[0].team] = []
            score[team[0].team] = 0
            for player in team:
                score[player.team] += len(self.all_kills.get(player.number, [])) * self.all_parameters[
                    'score_by_kill_one']
                team_save[player.team].append(player.number)

        # now deal with out order
        team_out_order = []
        self.print_debug(0, 'all players death order and frame:', self.die_order)
        for number, frame in self.die_order:
            team_number = self.number_to_player[number].team
            team_save[team_number].remove(number)
            if not len(team_save[team_number]):
                team_out_order.append((team_number, frame))
                team_save.pop(team_number)

        # if there is any team alive, must be one team with chicken dinner
        assert len(team_save) <= 1
        if len(team_save):
            team_out_order.append((team_save.popitem()[0], self.__turn + 1))

        # get score for each one's rank
        for rank in range(-1, -len(team_out_order) - 1, -1):
            team_number, frame = team_out_order[rank]
            score[team_number] += self.all_parameters['score_by_rank'].get(str(-rank), 0) if frame else 0

        # output result information
        self.print_debug(0, "all teams' scores are:", score)
        result = {
            'score': score,
            'team_out_order': team_out_order,
            'order_of_death': self.die_order,
        }
        with open(self.playback_file.name[:-2] + '.json', 'w') as file:
            dump(result, file)

        self.playback_file.close()
        return

    def print_debug(self, level, *args, sep=' ', end='\n', file=None):
        # print debug log if current debug level is higher than message debug level
        if self.__debug_level >= level:
            print(*args, sep=sep, end=end, file=file)


if __name__ == '__main__':
    # if necessary, test here
    pass
