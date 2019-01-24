# example-service

Simple arithmetic service compatible with SingularityNET

## Getting Started

### Prerequisites

* [Python 3.6.5](https://www.python.org/downloads/release/python-365/)

### Installing

* Clone the git repository:

```
$ git clone git@github.com:singnet/example-service.git
$ cd example-service
```

* Install the dependencies and compile the protobuf file:

```
$ pip3 install -r requirements.txt
$ sh buildproto.sh
```

### Running

#### Standalone

* Run the example service directly (without `SNET Daemon`):

```
$ python3 run_example_service.py --no-daemon
```

* To test it run the script:

```
$ python3 test_example_service.py
```

#### With SingularityNET Daemon

##### SingularityNET Daemon Configuration

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service 
(check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`).

```
{
   "DAEMON_END_POINT": "http://DAEMON_HOST:DAEMON_PORT",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://JSON_RPC_ENDPOINT",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "REGISTRY_ADDRESS",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://SERVICE_GRPC_HOST:SERVICE_GRPC_PORT",
   "ORGANIZATION_ID": "ORGANIZATION_ID",
   "SERVICE_ID": "SERVICE_ID",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
            "TYPE": "stdout"
           }
   }
}
```

For example, using the Kovan testnet, replace tags with:

- `http://DAEMON_HOST:DAEMON_PORT`: http://localhost:7000
- `https://JSON_RPC_ENDPOINT`: https://kovan.infura.io
- `REGISTRY_ADDRESS`: 0xe331bf20044a5b24c1a744abc90c1fd711d2c08d
- `http://SERVICE_GRPC_HOST:SERVICE_GRPC_PORT`: http://localhost:7003
- `ORGANIZATION_ID`: example-organization
- `SERVICE_ID`: example-service

For example, using the Ropsten testnet, replace tags with:

- `http://DAEMON_HOST:DAEMON_PORT`: http://localhost:7001
- `https://JSON_RPC_ENDPOINT`: https://ropsten.infura.io
- `REGISTRY_ADDRESS`: 0x5156fde2ca71da4398f8c76763c41bc9633875e4
- `http://SERVICE_GRPC_HOST:SERVICE_GRPC_PORT`: http://localhost:7003
- `ORGANIZATION_ID`: example-organization
- `SERVICE_ID`: example-service

See [SingularityNet daemon configuration](https://github.com/singnet/snet-daemon/blob/master/README.md#configuration) for detailed configuration description.

##### Running Service + Daemon on Host

* Run the script without flag to launch both `SNET Daemon` and the service

```
$ python3 run_example_service.py
```

##### Running Service + Daemon in Docker Container

* Build the docker image and run a Container from it:

```
$ docker build -t snet_example_service https://github.com/singnet/example-service.git#master
$ export ETCD_HOST_FOLDER=$HOME/singnet/etcd/example-service/
$ export ETCD_CONTAINER_FOLDER=/opt/singnet/example-service/storage-data-dir-1.etcd/
$ docker run -p 7000:7000 -v $ETCD_HOST_FOLDER:$ETCD_CONTAINER_FOLDER -ti snet_example_service bash
```

Note that the `$ETCD_(HOST|CONTAINER)_FOLDER` are useful to keep your service's etcd folder outside the container.

From this point we follow the tutorial in the Docker Container's prompt.

After this, run the service (with `SNET Daemon`), make sure you have the `snetd.config.json` file in the service folder:

```
# cat snetd.config.json
{
   "DAEMON_END_POINT": "http://localhost:7000",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "example-organization",
   "SERVICE_ID": "example-service",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
            "TYPE": "stdout"
           }
   }
}
# python3 run_example_service.py &
```

### Testing

* Invoke the test script (from the same Docker Container):

```
# python3 test_example_service.py
```

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/singnet/example-service/blob/master/LICENSE) file for details.
