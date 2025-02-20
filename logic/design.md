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
10. `terrain.py`:define class `Block`, `Area`, `Map` for the map
11. `circle.py`: define class `Circle` for the circle

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

`die_list`: die order in this frame, this will be given to platform

`map_items`:save id for all items in the map by multiway tree

`map`: map information for the game, an instance of class Map

`all_players`: save all teams as list, in which are all players' pointers

`all_bullets`:save id for all bullets(mainly shells) in the map

`all_sounds`:save all sounds(including footstep and guns) in the map

`all_wild_items`: a dictionary to save all items on the ground(maybe not wild but discarded)

`all_info`: a dictionary to save all players basic information for platform

`circle`: data for poison circle

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

`block_view`: means whether an object will block player's view

#### method

`is_intersecting`: given two end points of a segment and judge if this segment will intersect the object

`is_bumped`: judge if the object will bump another object

`is_opaque`: judge if the object is not transparent(from game's respective, it means the object is not high)

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

`get_polar_position`: input a vector direction and another position to get relative polar position

`pick_accessible`: give another position and judge if two positions are in picking range

`get_area_id`: get area id for this position

`distance_to_segment`: give two nodes positions and calculate the distance from self to the segment

`distacne_to_rectangle`: give a rectangle's center position, radius and angle ,calculate shortest distance from self to the edge of rectangle, and return -1 when self is in the rectangle

#### other function

also, I use some other functions to deal with two postioin

`delta_y`:get the delta of y of two position

`delta_x`:get the delta of x of two position

`dot_product`:get the dot product of two vector

`cross_product`:get the cross product of two vector

`angle_to_position`: get a unit vector by angle

`segments_intersected`: give two segments' end points and judge if the two segments will intersect

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

`health_point_limit`: max HP

`health_point`: current HP

`bag`: a dictionary for player's bag

`status`: player's current status

`move_cd`:

`shoot_cd:`

`vocation`: the player's vocation, should be one of vocation enumeration

`team`: save team id

`view_distance`: player's furthest view distance

 `view_angle`: player's largest view angle

`jump_position`: means where should the player jump out of airplane

`land_position`: the position of the player landing

`last_weapon`: save the last used/picked weapon's index

`best_armor`: save the best armor's id on the body

`block`: means which block is the player standing on(None for default)

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

`can_make_footsteps`: return if player can make footstep noise, depending on the status, maybe also on terrain and some items in the future

`get_damage`: get given value damage, parameter may cause to special effective

### `Sound`

(this class isn't inherited from Object because it's not entity)

#### enumeration

##### sound type

- RADIO_VOICE
- FOOTSTEP_SOUND
- GUN_SOUND
- BOOM_SOUND

#### attribute

##### static

`speed`:a dictionary to save different sounds' speed, assigned by data file

`farthest`: a dictionary to save different sounds' max transmission distance

##### dynamic

`sound_type`:  one of the sound type enumeration

`emitter`: the id of emitter

`receiver`: the id of receiver

`emitter_position`: emitter's position

`data`: the signal of radio

`__delay`: the delay frames for this sound to transmit

`delay`: save the total delay

#### method

##### static

`__load_data`: load data, mainly speed of different sound

##### dynamic

`update`: update __delay

`arrived`: judge if the signal has arrived in this frame

`get_data`: for radio, it will return data; for environment sound, it will generate data by bit manipulation

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

`data`: point to data for this type of item

`durability`: using durability, for vest it means how many damage it can block, for WEAPON it means bullets,and for GOODS it means rest using times

`item_type`: it should be a number according to data file

`id`: id of the item

#### method

##### static

`load_data`: load data from data file

`add`: add a new item entity and update next_id, then return this item's id

`remove`: remove a item from `all_items` by id

`get_data_by_item_id`: get item data by given item id

`get_random_item`: get a random item to put in the map based on `occur`

`get_reward_item`: get a random reward item better than normal for a code case

##### dynamic

`is_weapon`: judge if this item is a weapon

`is_armor`: judge if this item is a armor

`is_goods`: judge if this item is a goods

### `Block`

class for each single

#### attribute

##### static

`tree_radius`: tree's radius, map file will omit this data

`next_id`: save next id should the block get

##### dynamic

`name`: type name of a block imported from interface

`id`: the unique id number for each block in the map

#### method

##### static

`genarate_block`: get a Block instance by name and parameter

##### dynamic

`set_rectangle`: set block position data as a rectangle

`set_circle`: set block position data as a circle

`get_id`: get next id and update next id 

### `Area`

#### attribute

##### static

`areas_template`: save all name:area pair for different kinds of areas as templates, will be clear after Map initializes 

##### dynamic

`blocks`: a list to save all blocks in an area

`name`: type name of a area imported from interface

`id`: id number for an area, in [0, 100)

#### method

#####  static

`load_data`: load interface's data file to get all map information

`generate_area`: generate an area by name and id number from template

### `Map`

#### attribute

dynamic

`all_areas`: a list to save all areas in the map

`all_blocks`: use a dictionary to save all blocks

`__getitem__`: get an area in the map by area index or (x, y) index pair or position

#### method

##### dynamic

`initialize`: add all areas in the map by file data, then clear `Area.areas_template` and build dictionary

`stand_permitted`: judge if a position in the map is access to stand for character

`acessible`: judge if two position in the map can bound a line without bumped block

##### static

`get_id_list`: get id list intersected by the line bounded by the two given positions

### `Information`

this is the information package for platform

#### attribute

##### dynamic

`player`: a pointer to a player

`vision`: a list for all entities the player can see in this frame

`sound`: a list for all sounds the player can hear in this frame

#### method

`clear`: clear the lists

### `Circle`

this is the information for the circle

#### attribute

`center_now`: current circle's center position

`center_next`: next circle's center position

`radius_now`: current circle's radius

`radius_next`: next circle's radius

`flag`: status flag for circle

`shrink`: radius' shrinking speed

`move`: center's moving speed

`edge`: the edge of the map

`damager_per_frame`: player out of circle get such damage per frame

`rest_frames`: rest frames for current status

`all_data`: all_data load from data file

`stage`: means circle stage to get data

#### method

`load_data`: load data file

`start`: start generate the circle

`update`: update the circle per frame

`get_next_center`: get next circle center after stage changed

`safe`: judge if a player's position is safe

`is_processing`: judge if the circle is shrinking or waiting