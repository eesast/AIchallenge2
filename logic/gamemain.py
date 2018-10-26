#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass import *
from random import randrange


class GameMain:
    # if not specified, platform needn't this class's members
    def __init__(self, file_path="./"):
        # first load some module data here
        character.Character.load_data(file_path)
        item.Item.load_data(file_path)

        # it's more like a define instead of an initialization
        self.map_size = 1000
        self.die_order = []  # save the player's dying order
        self.map_items = [[[] for i in range(16)] for j in range(16)]  # try to divide map into 256 parts
        self.all_players = []
        self.number_to_player = {}  # use a number to find a player
        self.__start_position, self.__over_position = None, None

        # here load map data
        self.__load_map(file_path)
        return

    def initialize(self):
        # if platform has trouble in initializing the global variable, I will use it instead
        pass

    def unwrap_commands(self, commands):
        # here unwrap all players' commands
        return

    def refresh(self):      # refresh a new frame according to the orders
        def instructions():
            # I need instruction API to finish legality detection
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
                            player.status = character.Character.JUMPING
                            player.position = player.jump_position
                            player.move_direction = (player.land_position - player.jump_position).unitize()
                            player.move_speed = character.Character.JUMPING_SPEED
                            player.move_cd = (player.land_position - player.jump_position).length() / player.move_speed
                        elif player.is_jumping():
                            player.status = character.Character.RELAX
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

        # what to return is a vital question for platform
        return

    def __load_map(self, parent_path="./"):
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
            # I hope platform can finish this part :D
            pass

        def get_pedal(aim_position):
            # these formulas are transformed from internet, I hope they're right
            aim_x, aim_y = aim_position.x, aim_position.y
            A = position.delta_y(self.__start_position, self.__over_position)
            B = - position.delta_x(self.__start_position, self.__over_position)
            C = - position.cross_product(self.__start_position, self.__over_position)
            x = (B * B * aim_x - A * B * aim_y-A * C) / (A * A + B * B)
            y = (A * A * aim_y - A * B * aim_y - B * C) / (A * A + B * B)
            return position.Position(x, y)

        aim_positions = []
        # here unwrap players' information and their land positions
        unwrap()
        # supposing I get teams * 4 positions

        # debug: test positions
        # well, I haven't test yet
        # debug code over

        player_number = 0
        for pos in aim_positions:
            player = self.number_to_player[player_number]
            if not isinstance(player, character.Character):
                raise Exception("wrong object for dict number_to_player, get a", type(player))
            # I hope it's a pointer, otherwise it's a huge bug
            player.land_position = pos
            player.jump_position = get_pedal(pos)
            player.status = character.Character.ON_PLANE
            player.move_direction = (self.__over_position - self.__start_position).unitize()
            player.move_speed = character.Character.AIRPLANE_SPEED
            player.move_cd = player.jump_position.length() / player.move_speed
        # now everything down, main operation starts
        # return first turn's information
        return self.refresh()


if __name__ == '__main__':
    # if necessary, test here
    pass
