# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: code-fix.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x63ode-fix.proto\x12\x07\x63odefix\"g\n\x04User\x12\x1c\n\x14practice_description\x18\x01 \x01(\t\x12\x17\n\x0ftarget_language\x18\x02 \x01(\t\x12\x15\n\rcompiler_info\x18\x03 \x01(\t\x12\x11\n\tuser_code\x18\x04 \x01(\t\"\x1b\n\x05Reply\x12\x12\n\nright_code\x18\x01 \x01(\t23\n\x08UserInfo\x12\'\n\x04Info\x12\r.codefix.User\x1a\x0e.codefix.Reply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'code_fix_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _USER._serialized_start = 27
    _USER._serialized_end = 130
    _REPLY._serialized_start = 132
    _REPLY._serialized_end = 159
    _USERINFO._serialized_start = 161
    _USERINFO._serialized_end = 212
# @@protoc_insertion_point(module_scope)
