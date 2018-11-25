# Smart Socket Blockchain POC

## Setup

* Setup a pyHS100 supported plug (see https://github.com/GadgetReactor/pyHS100/blob/master/README.md) with meter function and connect it to your network.
* Install the hyperledger composer enviroment on your machine (https://hyperledger.github.io/composer/v0.19/introduction/introduction.html) and start the playground:
```composer-playground``` 
* Build the business-network:
```
cd businessnetwork
npm install
cd ..
composer archive create --sourceType dir --sourceName businessnetwork  -a smartsocket-network.bna
```
Next, import the business network.
* Create and start the rest API server: 
```
composer-rest-server -c USER@NETWORKCARD -n required -u true
```
* Install python dependencies

## Usage

```
usage: tplink.py [-h] [--ip PLUG_IP] --supplier SUPPLIER_ID --plug PLUG_ID
                 [--api-base APIBASE]

Run smart socket demo process

optional arguments:
  -h, --help            show this help message and exit
  --ip PLUG_IP          ip address of the H110 compatible smart socket. If no
                        ip is given, the tool will try to discover sockets and
                        will use the first one found.
  --supplier SUPPLIER_ID
                        EnergySupplier id
  --plug PLUG_ID        Plug id
  --api-base APIBASE    Base URI of the hyperledger composer REST api.
                        (default: http://localhost:3000/api/)
```

* Create at least one plug instance and one EnergySupplier instance.
* Make sure the business network is running and the rest API server is started correctly.
* Run the python script:
```
./tplink.py --supplier 1234 --plug 5678
```
Use control-C to stop the demo.
* Plug a load into the smart socket (eg. a light bulb)
* As you can see, the smart socket will switch on after a given time (and off again), a bonus instance 
and an energy amount instance is created (see the composer playground). After that, the bonus and consumption
values are multiplied and added to the current balance of the plug.
