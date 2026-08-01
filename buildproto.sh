#! /bin/bash
echo `pwd`
python3  -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. singnet/snet-daemon/pricing/pricing.proto --proto_path=/home/adminaccount/singnet/src
python3  -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. singnet/snet-daemon/training/training.proto --proto_path=/home/adminaccount/singnet/src
python3  -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/service_spec/example_service.proto --proto_path=/home/adminaccount/singnet/src
