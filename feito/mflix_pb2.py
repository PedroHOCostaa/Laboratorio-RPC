# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mflix.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'mflix.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmflix.proto\x12\x05mflix\"u\n\x05\x46ilme\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06titulo\x18\x02 \x01(\t\x12\x11\n\tdiretores\x18\x03 \x03(\t\x12\x0b\n\x03\x61no\x18\x04 \x01(\x05\x12\x0e\n\x06\x61tores\x18\x05 \x03(\t\x12\x0f\n\x07generos\x18\x06 \x03(\t\x12\x0f\n\x07\x64uracao\x18\x07 \x01(\x05\"&\n\x06\x46ilmes\x12\x1c\n\x06\x66ilmes\x18\x01 \x03(\x0b\x32\x0c.mflix.Filme\"?\n\x06Pedido\x12\n\n\x02op\x18\x01 \x01(\x05\x12\x1b\n\x05\x66ilme\x18\x02 \x01(\x0b\x32\x0c.mflix.Filme\x12\x0c\n\x04\x66unc\x18\x03 \x01(\x05\"i\n\x0b\x43onfirmacao\x12\x11\n\tresultado\x18\x01 \x01(\x05\x12\x1b\n\x05\x66ilme\x18\x02 \x01(\x0b\x32\x0c.mflix.Filme\x12\x1c\n\x06\x66ilmes\x18\x03 \x03(\x0b\x32\x0c.mflix.Filme\x12\x0c\n\x04\x65rro\x18\x04 \x01(\x05\x32\xc6\x02\n\x05Mflix\x12\x31\n\nCriarFilme\x12\r.mflix.Pedido\x1a\x12.mflix.Confirmacao\"\x00\x12\x30\n\tReadFilme\x12\r.mflix.Pedido\x1a\x12.mflix.Confirmacao\"\x00\x12\x32\n\x0bUpdateFilme\x12\r.mflix.Pedido\x1a\x12.mflix.Confirmacao\"\x00\x12\x32\n\x0b\x44\x65leteFilme\x12\r.mflix.Pedido\x1a\x12.mflix.Confirmacao\"\x00\x12\x36\n\x0fListaFilmesAtor\x12\r.mflix.Pedido\x1a\x12.mflix.Confirmacao\"\x00\x12\x38\n\x11ListaFilmesGenero\x12\r.mflix.Pedido\x1a\x12.mflix.Confirmacao\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mflix_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FILME']._serialized_start=22
  _globals['_FILME']._serialized_end=139
  _globals['_FILMES']._serialized_start=141
  _globals['_FILMES']._serialized_end=179
  _globals['_PEDIDO']._serialized_start=181
  _globals['_PEDIDO']._serialized_end=244
  _globals['_CONFIRMACAO']._serialized_start=246
  _globals['_CONFIRMACAO']._serialized_end=351
  _globals['_MFLIX']._serialized_start=354
  _globals['_MFLIX']._serialized_end=680
# @@protoc_insertion_point(module_scope)
