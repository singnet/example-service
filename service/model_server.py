import sys
import logging
import time
import uuid

import grpc
import concurrent.futures as futures

import service.common

# Importing the generated codes from buildproto.sh
import singnet.snet_daemon.training.training_pb2_grpc as grpc_bt_grpc
from singnet.snet_daemon.training.training_pb2 import  ModelDetailsResponse
from singnet.snet_daemon.training.training_pb2 import  IN_PROGRESS
from singnet.snet_daemon.training.training_pb2 import  CREATED
from singnet.snet_daemon.training.training_pb2 import  COMPLETED

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("model_training")


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class ModelServicer(grpc_bt_grpc.ModelServicer):
    def __init__(self):

        # Just for debugging purpose.
        log.debug("ModelServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def create_model(self, request, context):
        log.debug("Create Model ")
        # To respond we need to create a Result() object (from .proto file)
        self.result = ModelDetailsResponse()
        self.result.model_id = "#CLientgeneratedModelId"
        self.result.status = CREATED
        return self.result

    def update_model_access(self, request, context):
        log.debug("Update Model ")
        # To respond we need to create a Result() object (from .proto file)
        self.result = ModelDetailsResponse()
        self.result.status = IN_PROGRESS
        return self.result

    def delete_model(self, request, context):

        log.debug("MODEL DELETED AT CLIENT END to....")
        # To respond we need to create a Result() object (from .proto file)
        self.result = ModelDetailsResponse()
        self.result.status = COMPLETED
        return self.result


    def get_model_details(self, request, context):
        # In our case, request is a Numbers() object (from .proto file)
        log.debug("Not needed to implement , just a dummy  ....")
        # To respond we need to create a Result() object (from .proto file)
        self.result = ModelDetailsResponse()
        self.result.status = IN_PROGRESS
        return self.result

    def get_training_status(self, request, context):
        # In our case, request is a Numbers() object (from .proto file)
        log.debug("get training status ")
        # To respond we need to create a Result() object (from .proto file)
        self.result = ModelDetailsResponse()
        self.result.status = IN_PROGRESS
        return self.result




