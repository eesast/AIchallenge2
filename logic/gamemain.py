#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass import *
import proto.logic_pb2 as pb2
from random import randrange
from json import load
import time
import struct

#   here define a debug level variable to debug print-oriented
#   remember: here is just a initial level for logic
#   platform may give another number in game_init
PRINT_DEBUG = 50


#   level 1: only print illegal information
#   level 2: also print some adjustment

#   level 8: give all players' jumping information
#   level 9: print initialize information for parachuting
#   level 10: print commands for each frame

#   level 50: print data length for proto
#   level 100: will give all information you can imagine, including config file

class GameMain:
    # if not specified, platform needn't this class's members
    map_size = 1000
    playback_file_path = None

    def __init__(self):

        # it's more like a define instead of an initialization
        self.die_order = []  # save the player's dying order
        self.map_items = [[[] for i in range(16)] for j in range(16)]  # try to divide map into 256 parts

        self.all_players = []  # save all teams and players
        self.all_bullets = []
        self.all_sounds = []
        self.all_items = []
        self.all_info = []  # save all information for platform
        self.all_commands = {"move": {}, "shoot": {}, "pickup": {}, "radio": {}}

        self.number_to_team = {}  # use a number to find a team
        self.number_to_player = {}  # use a number to find a player
        self.__start_position, self.__over_position = None, None
        self.__turn = 0

        # initialize debug level for logic to use directly and for platform to change it
        self.__debug_level = PRINT_DEBUG

        return

    def set_debug_level(self, level):
        if level:
            self.__debug_level = level
        return

    def load_data(self, file_path, file_name):
        # first load some global information
        with open(file_path + file_name) as config:
            global_config = load(config)
        self.print_debug(100, global_config)

        # then load some module data here
        self.print_debug(100, character.Character.load_data(file_path, global_config["CHARACTER_FILE_PATH"]))
        self.print_debug(100, item.Item.load_data(file_path, global_config["ITEM_FILE_PATH"]))

        # here load map data
        self.__load_map(file_path, global_config["MAP_FILE_PATH"])

        # for play back file
        GameMain.playback_file_path = global_config["PLAYBACK_FILE_PATH"] + time.strftime("%Y%m%d_%H'%M'%S") + ".pb"
        open(GameMain.playback_file_path, 'wb').close()     # create the new playback file

    def write_playback(self, pb2_data):
        data = pb2_data.SerializeToString()
        with open(self.playback_file_path, 'ab') as playback:
            playback.write(struct.pack('i', len(data)))
            playback.write(data)
        self.print_debug(50, "write", len(data), "bytes into the playback file")

    def unwrap_commands(self, commands):
        # here unwrap all players' commands
        self.all_commands["move"].clear()
        self.all_commands["shoot"].clear()
        self.all_commands["pickup"].clear()
        self.all_commands["radio"].clear()
        # commands format: {teamID:{playerID:[{"command_tye":type, "target":
        # ID, "move_angle":angle, "view_angle":angle, "other":data}]}}

        self.print_debug(10, commands)
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
        self.print_debug(10, "unwrap_command successfully in turn", self.__turn)
        return

    def __load_map(self, parent_path, map_file_path):
        with open(parent_path + map_file_path, "r", encoding="utf-8") as map_file:
            self.map_size = 1000
            pass

    def alive_teams(self):
        alive_count = 0
        for team in self.all_players:
            for player in team:
                # check if there is at least one alive player in this team
                if player.heal_point > 0:
                    alive_count = alive_count + 1
                    break
                else:
                    continue
        return alive_count

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
            # these formulas are transformed from internet, I hope they're right
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
            data = pb2.InitialInfo()
            data.start.x, data.start.y = self.__start_position.x, self.__start_position.y
            data.over.x, data.over.y = self.__over_position.x, self.__over_position.y
            for each_team in self.all_players:
                for each_player in each_team:
                    player_info = data.players.add()
                    player_info.id = each_player.number
                    player_info.team = each_player.team
                    player_info.vocation = each_player.vocation
                    player_info.HP_max = int(each_player.heal_point)     # now HP == HP_max
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
                player.status = character.Character.ON_PLANE
                player.move_direction = (self.__over_position - self.__start_position).unitize()
                player.position = self.__start_position
                player.move_speed = character.Character.AIRPLANE_SPEED
                player.move_cd = int(player.jump_position.length() / player.move_speed + 1)
                player.face_direction = player.move_direction
                # meanwhile deal with information list
                self.all_info.append(info.Information(player))

        # output data for interface
        self.write_playback(get_proto_data())

        # now everything down, main operation starts
        # return first turn's information
        return self.refresh()

    def refresh(self):  # refresh a new frame according to the orders
        def instructions():
            for player_number, command in self.all_commands["pickup"].items():
                # if self.number_to_player[player_number].status != c
                pass

        def move():
            for team in self.all_players:
                for player in team:
                    if not isinstance(player, character.Character):
                        raise Exception("wrong player!")
                    player.move()

        def attack():
            pass

        def damage():
            pass

        def die():
            pass

        def items():
            pass

        def radio():
            pass

        def update():
            for team in self.all_players:
                for player in team:
                    if not isinstance(player, character.Character):
                        raise Exception("wrong player!")
                    if player.move_cd:
                        player.move_cd -= 1
                    if player.move_cd == 0:

                        if player.is_flying():
                            # this is change from flying to jumping
                            player.status = character.Character.JUMPING
                            player.position = player.jump_position
                            player.move_direction = (player.land_position - player.jump_position).unitize()
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
            return

        def get_proto_data():
            data = pb2.FrameInfo()
            data.frame = self.__turn
            for team in self.all_players:
                for player in team:
                    if player.is_flying() or not player.is_alive():
                        continue
                    elif player.is_jumping():
                        new_info = data.parachutists.add()
                        new_info.id = player.number
                        new_info.HP = int(player.heal_point)
                        new_info.face_direction = player.face_direction.get_angle()
                        new_info.pos.x, new_info.pos.y = player.position.x, player.position.y
                        new_info.jump_pos.x, new_info.jump_pos.y = player.jump_position.x, player.jump_position.y
                        new_info.land_pos.x, new_info.land_pos.y = player.land_position.x, player.land_position.y
                    else:
                        new_info = data.players.add()
                        new_info.id = player.number
                        new_info.HP = int(player.heal_point)
                        new_info.pos.x, new_info.pos.y = player.position.x, player.position.y
                        new_info.weapon = player.last_weapon
                        new_info.armor = player.best_armor
                        new_info.face_direction = player.face_direction.get_angle()
            return data

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

        # 7. refresh radio voice
        radio()

        # 8. update player's view, cd and etc
        update()

        self.__turn = self.__turn + 1

        # output data for playback file
        self.write_playback(get_proto_data())

        # return pack data after refreshing
        return self.pack_for_platform()

    # here return everything as i mention in the related files
    def pack_for_platform(self):

        return self.all_info

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
