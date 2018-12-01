#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass import *
from random import randrange
from json import load


class GameMain:
    # if not specified, platform needn't this class's members
    def __init__(self):

        # it's more like a define instead of an initialization
        self.map_size = 1000
        self.die_order = []  # save the player's dying order
        self.map_items = [[[] for i in range(16)] for j in range(16)]  # try to divide map into 256 parts
        self.all_players = []  # save all player's information
        self.all_bullets = []
        self.all_sounds = []
        self.all_items = []
        self.all_info = []  # save all information for platform
        self.all_commands = {"move": {}, "shoot": {}, "pickup": {}, "radio": {}}

        self.number_to_team = {}  # use a number to find a team
        self.number_to_player = {}  # use a number to find a player
        self.__start_position, self.__over_position = None, None
        self.__turn = 0

        return

    def load_data(self, file_path, file_name):
        def load_global():
            with open(file_path + file_name) as config:
                global_config = load(config)
            object.PRINT_DEBUG = global_config["PRINT_DEBUG"]
            object.CHARACTER_FILE_PATH = global_config["CHARACTER_FILE_PATH"]
            object.ITEM_FILE_PATH = global_config["ITEM_FILE_PATH"]
            object.MAP_FILE_PATH = global_config["MAP_FILE_PATH"]
            if object.PRINT_DEBUG >= 100:
                print(global_config)

        # first load some global information
        load_global()

        # then load some module data here
        character.Character.load_data(file_path, object.PRINT_DEBUG)
        item.Item.load_data(file_path)

        # here load map data
        self.__load_map(file_path)

    def unwrap_commands(self, commands):
        # here unwrap all players' commands
        self.all_commands["move"].clear()
        self.all_commands["shoot"].clear()
        self.all_commands["pickup"].clear()
        self.all_commands["radio"].clear()
        # commands format: {teamID:{playerID:[{"command_tye":type, "target":
        # ID, "move_angle":angle, "view_angle":angle, "other":data}]}}
        # for debug
        commands = \
            {
                5: [
                    {'command_type': 1, 'target': 12, "move_angle": 1.2, "view_angle": 3.6, "other": 13}
                ],
            }
        if object.PRINT_DEBUG >= 10:
            print(commands)
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
        if object.PRINT_DEBUG >= 10:
            print("unwrap_command successfully in turn", self.__turn)
        return

    def refresh(self):  # refresh a new frame according to the orders
        def instructions():
            for player_number, command in self.all_commands["pickup"].items():
                # if self.number_to_player[player_number].state != c
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
                            player.state = character.Character.JUMPING
                            player.position = player.jump_position
                            player.move_direction = (player.land_position - player.jump_position).unitize()
                            player.move_speed = character.Character.JUMPING_SPEED
                            player.move_cd = int((player.land_position - player.jump_position).length() /
                                                 player.move_speed + 1)
                            player.face_direction = player.move_direction
                        elif player.is_jumping():
                            # jump to the land, and then relax
                            player.state = character.Character.RELAX
                            player.position = player.land_position
                            player.move_direction = None
                            player.move_speed = 0

            pass

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

        # here return everything as i mention in the related files
        return self.all_info

    def __load_map(self, parent_path="./"):
        with open(parent_path + object.MAP_FILE_PATH, "r", encoding="utf-8") as map_file:
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
                    if object.PRINT_DEBUG:
                        print("number", player_number, "choose illegal vocation", new_vocation)
                    new_vocation = 0

                # then ensure it hasn't been chosen, or I will give one
                for player_check in self.number_to_team[team_number]:
                    if new_vocation == player_check.vocation:
                        if object.PRINT_DEBUG:
                            print("player", player_number, "choose repeated vocation", new_vocation, end='')
                            print("(this log maybe repeated during trying to adjust vocation )")
                        new_vocation = (new_vocation + 1) % character.Character.VOCATION_COUNT

                new_player = character.Character(new_vocation)
                new_player.land_position = position.Position(player_information['position'])
                if not new_player.land_position.good(self.map_size):  # for illegal aim, auto fall in the end
                    if object.PRINT_DEBUG:
                        print("number", player_number, "choose illegal aim", new_player.land_position)
                    new_player.land_position = self.__over_position
                new_player.number = player_number
                new_team.append(new_player)
                self.number_to_player[player_number] = new_player
            return

        def get_pedal(aim_position, number=-1):
            # these formulas are transformed from internet, I hope they're right
            aim_x, aim_y = aim_position.x, aim_position.y
            a = position.delta_y(self.__start_position, self.__over_position)
            b = - position.delta_x(self.__start_position, self.__over_position)
            c = position.cross_product(self.__start_position, self.__over_position)
            x = (b * b * aim_x - a * b * aim_y - a * b) / (a * a + b * b)
            y = (a * a * aim_y - a * b * aim_y - b * b) / (a * a + b * b)
            aim = position.Position(x, y)
            # if the pedal isn't in the map, player must jump at begin or end
            if x < 0 or y < 0 or x > self.map_size or y > self.map_size:
                if object.PRINT_DEBUG >= 2:
                    print("player", number, "aimed", aim_position, "pedal is", aim, end='')
                aim = self.__start_position if aim.distance2(self.__start_position) < aim.distance2(
                    self.__over_position) else self.__over_position
                if object.PRINT_DEBUG >= 2:
                    print("now it has been adjusted to", aim)
            return aim

        if object.PRINT_DEBUG >= 9:
            print('parachute:' + str(information))

        # here unwrap players' information and their land positions
        unwrap()

        # I just got teams information for the first time, now save them
        for team in self.all_players:
            for player in team:
                if not isinstance(player, character.Character):
                    raise Exception("wrong object for dict number_to_player, get a", type(player))
                # I hope it's a pointer, otherwise it's a huge bug
                player.jump_position = get_pedal(player.land_position, player.number)
                player.state = character.Character.ON_PLANE
                player.move_direction = (self.__over_position - self.__start_position).unitize()
                player.position = self.__start_position
                player.move_speed = character.Character.AIRPLANE_SPEED
                player.move_cd = int(player.jump_position.length() / player.move_speed + 1)
                player.face_direction = player.move_direction
                # meanwhile deal with information list
                self.all_info.append(info.Information(player))
        # now everything down, main operation starts
        # return first turn's information
        return self.refresh()

    def anti_infinite_loop(self):
        # the game can hold no more than half an hour
        # later, we will design poison circle, but now I can just use enforcement measure
        return self.__turn < 20 * 60 * 30


if __name__ == '__main__':
    # if necessary, test here
    pass
