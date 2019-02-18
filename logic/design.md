[TOC]

# design

This file is for logic to organize the whole project.

## source files

1. `main.py`:platform will import this file to get API, and logic will test here
2. `gamemain.py`:here define the main class for game: `GameMain`.all orders and game management will be processed.
3. `__init__.py`:initialize package `allclass`
4. `object.py`:define basic class `Object` for all entities
5. `info.py`:define class `Information` for platform
6. `item.py`:define class `Item` for all pick-ups
7. `character.py`:define class `Character` to define players
8. `position.py`:define class `Position` for game position process
9. `sound.py`:define class `Sound` for footstep, gun, radio and etc.
10. `vision.py`:define class `LandForm` for static items in the map and `Vision` for character's vision

## Class

### `GameMain`

here is the main class for the whole game, and it is a singleton class.

#### attribute

remember: all containers here consist of just id, while the entities exist as class's static members.

##### static

`map_size`: the length of edge of the map

`playback_file_path`: the path for playback file

##### dynamic

`die_order`:save the order of players' death by player id

`map_items`:save id for all items in the map by multiway tree

`all_players`: save all teams as list, in which are all players' pointers

`all_bullets`:save id for all bullets(mainly shells) in the map

`all_sounds`:save all sounds(including footstep and guns) in the map

`all_wild_items`: a dictionary to save all items on the ground(maybe not wild but discarded)

`all_info`: a dictionary to save all players basic information for platform

`number_to_team`:use team id to find a team's pointer

`number_to_player`:use player id to find a player's pointer

`__start_position`:the start position of the route, it's a `(float,float)`

`__over_position`:the over position of the route, it's a `(float,float)`

`__turn`:current turns, `int`

`__debug_level`:the debug level of the game manager, for logic it is PRINT_DEBUG,for platform it's defined in the game_init

#### method

`set_debug_level`:set debug level, mainly for platform

`load_data`:load config file, character data file, item data file and map file

`map_init`: initialize the map, mainly layout some airdrops randomly

`unwrap_commands`:after receive commands from platform, use this method to unwrap them

`__load_map`:load map data from file by interface

`alive_teams`: judge number of alive teams in the map to judge if game over

`generate_route`:generate the route of plane, here are other two functions, `random_route` to get a route and return start position and over position, `get_position` use a parameter as distance to get a position, whose algorithm is to find along the edge of map anti-clock-wisely for given distance

`parachute`:deal with parachute event, here are other three functions, `unwrap` to unwrap player initial information and `get_pedal` to get the pedal , `get_proto_data` to get `InitialInfo` data for interface

`refresh`:refresh game in each turn. Here are other functions, including `instructions`, `move`, `attack`, `damage`,` die`,` items`, `noise`,` update` for all eight stages, as well as `get_proto_data` to get `FrameInfo` data

`pack_for_platform`: pack data as proto for platform to return each frame

`write_playback`: write a proto object into playback file

`anti_infinite_loop`:judge if the game have lasted too long

`print_debug`: the main API for platform and logic to get debug log

### `Object`  

the abstract basic class for all other entities in the game

#### attribute

##### static

`CIRCLE`: 0, the id for circle entity

`RECTANGLE`: 1, the id for rectangle entity

##### dynamic

`position`:the position for object

`shape`:the shape of object, it should be CIRCLE or RECTANGLE

`move_speed`:the move speed of this object

`number`:the id of object

`move_direction`:the move direction of this object, it should use a position as a vector

`face_direction`:the face direction of this object, it should use a position as a vector

`radius`:the radius for circle and half diagonal length for rectangle

`angle`:for rectangle, it means included angles in the right

### `Position`

generally speaking, this class has two usage, as a position in the map or as a vector to deal with math operation

#### attribute

`x`:a `float`

`y`:a `float`

#### method

`__add__`:add two positions by '+'

`__sub__`:substract two positions by '-'

`__abs__`:get length of position from origin

`__mul__`:get dot product by another position or product a number to enlarge by  using '*'

`__truediv__`:use '/' just as `__mul__`

`length`:get the length of position from origin

`length2`:get the length's square

`distance`:get the length of this position from another position

`distance2`:get distance's square

`unitize`:unitize this vector by not giving another one or use this vector as unite to unitize another vector

`good`:judge if this position is in the map

`get angle`: get angle in [0, 360) for the direction of the vector

#### other function

also, I use some other functions to deal with two postioin

`delta_y`:get the delta of y of two position

`delta_x`:get the delta of x of two position

`dot_product`:get the dot product of two vector

`cross_product`:get the cross product of two vector

`angle_to_position`: get a unit vector by angle

### `Character`

inherited from Object(CIRCLE), define player's entity

#### enumeration

##### vocation

- MEDIC
- ENGINEER
- SIGNALMAN
- HACK
- SNIPER
- VOCATION_COUNT

##### status

<!--this may be updated in the future-->

- RELAX: normal status
- ON_PLANE: before jumping
- JUMPING: while jumping to the land
- MOVING: when the player is just moving
- SHOOTING: when the player is standing to shoot
- PICKUP:  before the player pick up the air-drop
- MOVING_SHOOTING: when the player is moving by shooting
- DEAD: it means one's HP declined to zero but still can be reborn
- REAL_DEAD: it means one is already eliminate  

#### attribute

##### static

`all_data`: load data from data file

`all_characters`: a dictionary to save all characters' entities by id-entity pair

`AIRLANE_SPEED`: the speed of airplane

`JUMPING_SPEED`: the speed of parachuting

<!--this will also be updated in the future-->

`MOVE_PERMITTED_STATUS`: a player is allowed to move if  his status is in this list

`SHOOTING_PREMITTED_STATUS`:a player is allowed to shoot if  his status is in this list

##### dynamic

`__heal_point_limit`: max HP

`heal_point`: current HP

`bag`: a list for player's bag

`status`: player's current status

`move_cd`:

`shoot_cd:`

`vocation`: the player's vocation, should be one of vocation enumeration

`jump_position`: means where should the player jump out of airplane

`land_position`: the position of the player landing

`last_weapon`: save the last used/picked weapon's id

`best_armor`: save the best armor's id on the body

#### method

##### static

`load_data`: load character data file

##### dynamic

`is_flying`: judge if the player is on the plane

`is_jumping`: judge if the player is jumping to the land

`is_alive`: judge if the player is still alive(not real dead)

`is_piking`: judge if player is picking something

`can_be_hit`: judge if player is alive so that can be bullet hit

`move`: deal with player move event, it will be complex, hasn't started to code yet

`command_status_legal`: judge if the given command is legal

`change_status`: change status and refresh some status related data

### `Sound`

(this class isn't inherited from Object because it's not entity)

#### enumeration

##### sound type

- FOOTSTEP_SOUND
- GUN_SOUND
- RADIO_VOICE

#### attribute

##### static

`SPEED`:a list to save different sounds' speed, assigned by data file

##### dynamic

`sound_type`:  one of the sound type enumeration

`emitter`: the id of emitter

`receiver`: the id of receiver

`distance`: the distance between emitter and receiver

`__speed`: the speed of this type of sound

`__delay`: the delay frames for this sound to transmit

`data`: the signal of radio

#### method

##### static

`__load_data`: load data, mainly speed of different sound

##### dynamic

`arrive`: judge if the signal has arrived in this frame

### `Item`

inherited from Object, the class of all pick-up in the map

#### enumeration

##### type

- WEAPON
- ARMOR
- GOODS

#### attribute

##### static

`all_data`: a dictionary to save all items data, loaded from data file

`all_items`: a dictionary to save all items' entities by id-entity pair

`next_id`: id should be monotone increasing, use this variable to get a new id

`string_to_type`: a dictionary to get item's type(WEAPON, ARMOR, GOODS) by string from data file

##### dynamic

`durability`: using durability, for vest it means how many damage it can block, for WEAPON it means bullets,and for GOODS it means rest using times

`item_type`: it should be a number according to data file

`id`: id of the item

`owner`: the id of player who owns it or -1 as default value

##### method

##### static

`load_data`: load data from data file

`add`: add a new item entity and update next_id, then return this item's id

##### dynamic

`is_weapon`: judge if this item is a weapon

`is_armor`: judge if this item is a armor

`is_goods`: judge if this item is a goods

### `LandForm`

this method defined all static entity in the map

#### enumeration

##### type

- WALL
- TREE

#### attribute

##### static

`CIRCLE_SHAPE`: the list for all circle landform

`RECTANGLE_SHAPE`: the list for all rectangle landform

##### dynamic

`land_type`: it should be type enumeration

#### method

<!--to be finished-->

### `Vision`

player's vision should be updated every frame

#### attribute

##### dynamic

`ID`: id of the entity

`distance`: the distance between the player and entity

`angle`: the angle between player's `face_direction` and the entity

#### method

<!--to be finished-->

### `Information`

this is the information package for platform

#### attribute

##### dynamic

`player`: a pointer to a player

`vision`: a list for all entities the player can see in this frame

`sound`: a list for all sounds the player can hear in this frame

#### method

`clear`: clear the lists