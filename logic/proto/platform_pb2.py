# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: platform.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='platform.proto',
  package='logic_to_platform',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0eplatform.proto\x12\x11logic_to_platform\"0\n\rPolarPosition\x12\x10\n\x08\x64istance\x18\x01 \x01(\x01\x12\r\n\x05\x61ngle\x18\x02 \x01(\x01\"\"\n\nXYPosition\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\"h\n\x04Item\x12\x0f\n\x07item_ID\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\x05\x12-\n\x03pos\x18\x03 \x01(\x0b\x32 .logic_to_platform.PolarPosition\x12\x12\n\ndurability\x18\x04 \x01(\x05\"\xcc\x01\n\nPoisonInfo\x12\x35\n\x0e\x63urrent_center\x18\x01 \x01(\x0b\x32\x1d.logic_to_platform.XYPosition\x12\x32\n\x0bnext_center\x18\x02 \x01(\x0b\x32\x1d.logic_to_platform.XYPosition\x12\x16\n\x0e\x63urrent_radius\x18\x03 \x01(\x01\x12\x13\n\x0bnext_radius\x18\x04 \x01(\x01\x12\x13\n\x0brest_frames\x18\x05 \x01(\x05\x12\x11\n\tmove_flag\x18\x06 \x01(\x05\"\xbb\x02\n\x08SelfInfo\x12\x14\n\x0chealth_point\x18\x01 \x01(\x01\x12\x1a\n\x12health_point_limit\x18\x02 \x01(\x01\x12\x12\n\nmove_angle\x18\x03 \x01(\x01\x12\x12\n\nview_angle\x18\x04 \x01(\x01\x12\x12\n\nmove_speed\x18\x05 \x01(\x01\x12\x10\n\x08vocation\x18\x06 \x01(\x05\x12\x0e\n\x06status\x18\x07 \x01(\x05\x12\x0f\n\x07move_cd\x18\x08 \x01(\x05\x12\x11\n\tattack_cd\x18\t \x01(\x05\x12*\n\x03pos\x18\n \x01(\x0b\x32\x1d.logic_to_platform.XYPosition\x12$\n\x03\x62\x61g\x18\x0b \x03(\x0b\x32\x17.logic_to_platform.Item\x12\x12\n\nview_width\x18\x0c \x01(\x01\x12\x15\n\rview_distance\x18\r \x01(\x01\"\xab\x01\n\tOtherInfo\x12\x11\n\tplayer_ID\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x05\x12\x12\n\nmove_angle\x18\x03 \x01(\x01\x12\x12\n\nview_angle\x18\x04 \x01(\x01\x12\x12\n\nmove_speed\x18\x05 \x01(\x01\x12\x10\n\x08vocation\x18\x06 \x01(\x05\x12-\n\x03pos\x18\x07 \x01(\x0b\x32 .logic_to_platform.PolarPosition\"9\n\x05Sound\x12\x0e\n\x06sender\x18\x01 \x01(\x05\x12\r\n\x05\x64\x65lay\x18\x02 \x01(\x05\x12\x11\n\tparameter\x18\x03 \x01(\x05\"\x8e\x02\n\nPlayerInfo\x12\x11\n\tplayer_ID\x18\x06 \x01(\x05\x12)\n\x04self\x18\x01 \x01(\x0b\x32\x1b.logic_to_platform.SelfInfo\x12\x13\n\x0blandform_id\x18\x02 \x03(\x05\x12&\n\x05items\x18\x03 \x03(\x0b\x32\x17.logic_to_platform.Item\x12,\n\x06others\x18\x04 \x03(\x0b\x32\x1c.logic_to_platform.OtherInfo\x12(\n\x06sounds\x18\x05 \x03(\x0b\x32\x18.logic_to_platform.Sound\x12-\n\x06poison\x18\x07 \x01(\x0b\x32\x1d.logic_to_platform.PoisonInfob\x06proto3')
)




_POLARPOSITION = _descriptor.Descriptor(
  name='PolarPosition',
  full_name='logic_to_platform.PolarPosition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='distance', full_name='logic_to_platform.PolarPosition.distance', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angle', full_name='logic_to_platform.PolarPosition.angle', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=85,
)


_XYPOSITION = _descriptor.Descriptor(
  name='XYPosition',
  full_name='logic_to_platform.XYPosition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='logic_to_platform.XYPosition.x', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='logic_to_platform.XYPosition.y', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=121,
)


_ITEM = _descriptor.Descriptor(
  name='Item',
  full_name='logic_to_platform.Item',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='item_ID', full_name='logic_to_platform.Item.item_ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='logic_to_platform.Item.type', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pos', full_name='logic_to_platform.Item.pos', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='durability', full_name='logic_to_platform.Item.durability', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=227,
)


_POISONINFO = _descriptor.Descriptor(
  name='PoisonInfo',
  full_name='logic_to_platform.PoisonInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_center', full_name='logic_to_platform.PoisonInfo.current_center', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_center', full_name='logic_to_platform.PoisonInfo.next_center', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='current_radius', full_name='logic_to_platform.PoisonInfo.current_radius', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_radius', full_name='logic_to_platform.PoisonInfo.next_radius', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rest_frames', full_name='logic_to_platform.PoisonInfo.rest_frames', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='move_flag', full_name='logic_to_platform.PoisonInfo.move_flag', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=230,
  serialized_end=434,
)


_SELFINFO = _descriptor.Descriptor(
  name='SelfInfo',
  full_name='logic_to_platform.SelfInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='health_point', full_name='logic_to_platform.SelfInfo.health_point', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='health_point_limit', full_name='logic_to_platform.SelfInfo.health_point_limit', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='move_angle', full_name='logic_to_platform.SelfInfo.move_angle', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view_angle', full_name='logic_to_platform.SelfInfo.view_angle', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='move_speed', full_name='logic_to_platform.SelfInfo.move_speed', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vocation', full_name='logic_to_platform.SelfInfo.vocation', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='logic_to_platform.SelfInfo.status', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='move_cd', full_name='logic_to_platform.SelfInfo.move_cd', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attack_cd', full_name='logic_to_platform.SelfInfo.attack_cd', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pos', full_name='logic_to_platform.SelfInfo.pos', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bag', full_name='logic_to_platform.SelfInfo.bag', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view_width', full_name='logic_to_platform.SelfInfo.view_width', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view_distance', full_name='logic_to_platform.SelfInfo.view_distance', index=12,
      number=13, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=437,
  serialized_end=752,
)


_OTHERINFO = _descriptor.Descriptor(
  name='OtherInfo',
  full_name='logic_to_platform.OtherInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_ID', full_name='logic_to_platform.OtherInfo.player_ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='logic_to_platform.OtherInfo.status', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='move_angle', full_name='logic_to_platform.OtherInfo.move_angle', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='view_angle', full_name='logic_to_platform.OtherInfo.view_angle', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='move_speed', full_name='logic_to_platform.OtherInfo.move_speed', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vocation', full_name='logic_to_platform.OtherInfo.vocation', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pos', full_name='logic_to_platform.OtherInfo.pos', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=755,
  serialized_end=926,
)


_SOUND = _descriptor.Descriptor(
  name='Sound',
  full_name='logic_to_platform.Sound',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='logic_to_platform.Sound.sender', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delay', full_name='logic_to_platform.Sound.delay', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameter', full_name='logic_to_platform.Sound.parameter', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=928,
  serialized_end=985,
)


_PLAYERINFO = _descriptor.Descriptor(
  name='PlayerInfo',
  full_name='logic_to_platform.PlayerInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_ID', full_name='logic_to_platform.PlayerInfo.player_ID', index=0,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='self', full_name='logic_to_platform.PlayerInfo.self', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='landform_id', full_name='logic_to_platform.PlayerInfo.landform_id', index=2,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='items', full_name='logic_to_platform.PlayerInfo.items', index=3,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='others', full_name='logic_to_platform.PlayerInfo.others', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sounds', full_name='logic_to_platform.PlayerInfo.sounds', index=5,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='poison', full_name='logic_to_platform.PlayerInfo.poison', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=988,
  serialized_end=1258,
)

_ITEM.fields_by_name['pos'].message_type = _POLARPOSITION
_POISONINFO.fields_by_name['current_center'].message_type = _XYPOSITION
_POISONINFO.fields_by_name['next_center'].message_type = _XYPOSITION
_SELFINFO.fields_by_name['pos'].message_type = _XYPOSITION
_SELFINFO.fields_by_name['bag'].message_type = _ITEM
_OTHERINFO.fields_by_name['pos'].message_type = _POLARPOSITION
_PLAYERINFO.fields_by_name['self'].message_type = _SELFINFO
_PLAYERINFO.fields_by_name['items'].message_type = _ITEM
_PLAYERINFO.fields_by_name['others'].message_type = _OTHERINFO
_PLAYERINFO.fields_by_name['sounds'].message_type = _SOUND
_PLAYERINFO.fields_by_name['poison'].message_type = _POISONINFO
DESCRIPTOR.message_types_by_name['PolarPosition'] = _POLARPOSITION
DESCRIPTOR.message_types_by_name['XYPosition'] = _XYPOSITION
DESCRIPTOR.message_types_by_name['Item'] = _ITEM
DESCRIPTOR.message_types_by_name['PoisonInfo'] = _POISONINFO
DESCRIPTOR.message_types_by_name['SelfInfo'] = _SELFINFO
DESCRIPTOR.message_types_by_name['OtherInfo'] = _OTHERINFO
DESCRIPTOR.message_types_by_name['Sound'] = _SOUND
DESCRIPTOR.message_types_by_name['PlayerInfo'] = _PLAYERINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PolarPosition = _reflection.GeneratedProtocolMessageType('PolarPosition', (_message.Message,), dict(
  DESCRIPTOR = _POLARPOSITION,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.PolarPosition)
  ))
_sym_db.RegisterMessage(PolarPosition)

XYPosition = _reflection.GeneratedProtocolMessageType('XYPosition', (_message.Message,), dict(
  DESCRIPTOR = _XYPOSITION,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.XYPosition)
  ))
_sym_db.RegisterMessage(XYPosition)

Item = _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), dict(
  DESCRIPTOR = _ITEM,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.Item)
  ))
_sym_db.RegisterMessage(Item)

PoisonInfo = _reflection.GeneratedProtocolMessageType('PoisonInfo', (_message.Message,), dict(
  DESCRIPTOR = _POISONINFO,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.PoisonInfo)
  ))
_sym_db.RegisterMessage(PoisonInfo)

SelfInfo = _reflection.GeneratedProtocolMessageType('SelfInfo', (_message.Message,), dict(
  DESCRIPTOR = _SELFINFO,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.SelfInfo)
  ))
_sym_db.RegisterMessage(SelfInfo)

OtherInfo = _reflection.GeneratedProtocolMessageType('OtherInfo', (_message.Message,), dict(
  DESCRIPTOR = _OTHERINFO,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.OtherInfo)
  ))
_sym_db.RegisterMessage(OtherInfo)

Sound = _reflection.GeneratedProtocolMessageType('Sound', (_message.Message,), dict(
  DESCRIPTOR = _SOUND,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.Sound)
  ))
_sym_db.RegisterMessage(Sound)

PlayerInfo = _reflection.GeneratedProtocolMessageType('PlayerInfo', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERINFO,
  __module__ = 'platform_pb2'
  # @@protoc_insertion_point(class_scope:logic_to_platform.PlayerInfo)
  ))
_sym_db.RegisterMessage(PlayerInfo)


# @@protoc_insertion_point(module_scope)
