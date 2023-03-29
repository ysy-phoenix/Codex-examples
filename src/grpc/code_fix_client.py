from __future__ import print_function

import logging, sys

import grpc
import code_fix_pb2
import code_fix_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stup = code_fix_pb2_grpc.UserInfoStub(channel)
        response = stup.Info(code_fix_pb2.User(
            practice_description="given two integer a and b, returns the sum of a and b",
            target_language="cpp",
            compiler_info="g++ -std=c++11 -O2 -Wall",
            user_code="#include <iostream> \n int main() \n{ return a + b; }"))
    print("修复后的代码：\n" + response.right_code)


if __name__ == '__main__':
    logging.basicConfig()
    run()
