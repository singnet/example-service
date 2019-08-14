from concurrent import futures
import contextlib
import datetime
import logging
import multiprocessing
import time
import socket
import sys

import argparse
import os
import grpc

from service import registry

# Importing the generated codes from buildproto.sh
import service.service_spec.example_service_pb2_grpc as grpc_bt_grpc
from service.service_spec.example_service_pb2 import Result

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s]"
                    " - %(name)s - %(message)s")
_LOGGER = logging.getLogger("example_service")

_ONE_DAY = datetime.timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT

"""
Simple arithmetic service to test the Snet Daemon (gRPC), dApp and/or Snet-CLI.
The user must provide the method (arithmetic operation) and
two numeric inputs: "a" and "b".

e.g:
With dApp:  'method': mul
            'params': {"a": 12.0, "b": 77.0}
Resulting:  response:
                value: 924.0


Full snet-cli cmd:
$ snet client call mul '{"a":12.0, "b":77.0}'

Result:
(Transaction info)
Signing job...

Read call params from cmdline...

Calling service...

    response:
        value: 924.0
"""

# Create a class to be added to the gRPC server
# derived from the protobuf codes.


class CalculatorServicer(grpc_bt_grpc.CalculatorServicer):
    def __init__(self):
        self.pid = os.getpid()
        self.a = 0
        self.b = 0
        self.result = 0
        # Just for debugging purpose.
        _LOGGER.debug("[{}] CalculatorServicer created".format(self.pid))

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def add(self, request, context):
        # In our case, request is a Numbers() object (from .proto file)
        self.a = request.a
        self.b = request.b

        # To respond we need to create a Result() object (from .proto file)
        self.result = Result()

        self.result.value = self.a + self.b
        _LOGGER.debug("[{}] add({},{})={}".format(self.pid,
                                                  self.a,
                                                  self.b,
                                                  self.result.value))
        return self.result

    def sub(self, request, context):
        self.a = request.a
        self.b = request.b

        self.result = Result()
        self.result.value = self.a - self.b
        _LOGGER.debug("[{}] sub({},{})={}".format(self.pid,
                                                  self.a,
                                                  self.b,
                                                  self.result.value))
        return self.result

    def mul(self, request, context):
        self.a = request.a
        self.b = request.b

        self.result = Result()
        self.result.value = self.a * self.b
        _LOGGER.debug("[{}] mul({},{})={}".format(self.pid,
                                                  self.a,
                                                  self.b,
                                                  self.result.value))
        return self.result

    def div(self, request, context):
        self.a = request.a
        self.b = request.b

        self.result = Result()
        self.result.value = self.a / self.b
        _LOGGER.debug("[{}] div({},{})={}".format(self.pid,
                                                  self.a,
                                                  self.b,
                                                  self.result.value))
        return self.result


def wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def run_server(grpc_port=7777):
    options = (('grpc.so_reuseport', 1),)
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=_THREAD_CONCURRENCY,),
        options=options)
    grpc_bt_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port("[::]:{}".format(grpc_port))
    server.start()
    wait_forever(server)


@contextlib.contextmanager
def reserve_port(grpc_port=7777):
    """Find and reserve a port for all subprocesses to use."""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', grpc_port))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()


def main():
    """ Runs the gRPC server to communicate with the SNET Daemon. """
    parser = argparse.ArgumentParser(prog=__file__)
    service_name = os.path.splitext(os.path.basename(__file__))[0]
    parser.add_argument("--grpc-port",
                        help="port to bind gRPC service to",
                        default=registry[service_name]['grpc'],
                        type=int,
                        required=False)
    parser.add_argument("--mp",
                        help="number of concurrent processes",
                        metavar="NUMBER_OF_PROCESSES",
                        default=1,
                        type=int,
                        required=False)
    args = parser.parse_args()

    num_processes = _PROCESS_COUNT if args.mp > _PROCESS_COUNT else args.mp
    with reserve_port(args.grpc_port) as port:
        sys.stdout.flush()
        workers = []
        for _ in range(num_processes):
            # NOTE: It is imperative that the worker subprocesses be forked before
            # any gRPC servers start up. See
            # https://github.com/grpc/grpc/issues/16001 for more details.
            worker = multiprocessing.Process(target=run_server, args=(port,))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()


if __name__ == "__main__":
    main()
