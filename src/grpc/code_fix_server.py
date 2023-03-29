from concurrent import futures
import logging

import grpc
import code_fix_pb2
import code_fix_pb2_grpc

from src.base import code_fix_api


class UserInfo(code_fix_pb2_grpc.UserInfoServicer):
    def Info(self, request, context):
        result = code_fix_api.find_solution(request.practice_description, request.target_language,
                                            request.compiler_info, request.user_code)
        return code_fix_pb2.Reply(right_code=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    code_fix_pb2_grpc.add_UserInfoServicer_to_server(UserInfo(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
