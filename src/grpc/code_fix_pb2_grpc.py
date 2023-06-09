# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import code_fix_pb2 as code__fix__pb2


class UserInfoStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Info = channel.unary_unary(
            '/codefix.UserInfo/Info',
            request_serializer=code__fix__pb2.User.SerializeToString,
            response_deserializer=code__fix__pb2.Reply.FromString,
        )


class UserInfoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserInfoServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Info': grpc.unary_unary_rpc_method_handler(
            servicer.Info,
            request_deserializer=code__fix__pb2.User.FromString,
            response_serializer=code__fix__pb2.Reply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'codefix.UserInfo', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class UserInfo(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Info(request,
             target,
             options=(),
             channel_credentials=None,
             call_credentials=None,
             insecure=False,
             compression=None,
             wait_for_ready=None,
             timeout=None,
             metadata=None):
        return grpc.experimental.unary_unary(request, target, '/codefix.UserInfo/Info',
                                             code__fix__pb2.User.SerializeToString,
                                             code__fix__pb2.Reply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
