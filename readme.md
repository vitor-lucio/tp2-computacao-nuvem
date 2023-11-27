# readme

playlist-rules-generator and server are built and pushed manually.

## to build and push playlist-rules-generator

if running locally, playlist-rules-generator should have a .env configured (main.py explains what env variables are needed)

`cd playlist-rules-generator/`


`docker build . -t vitorlucio/tp2-rules-generator:latest --no-cache`


`docker push vitorlucio/tp2-rules-generator:latest`

## to build and push server

if running locally, server should have a .env configured (main.py explains what env variables are needed)

`cd server/`

`docker build . -t vitorlucio/tp2-server:<same_tag_as_in_deployment.yaml> --no-cache`

`docker push vitorlucio/tp2-server:<same_tag_as_in_deployment.yaml>`

## to run client

client should have a .env file like the exemplo.env file inside the client folder, containing the server's reachable host in SERVER_NAME and server's reachable port in SERVER_PORT.

The server port in kubernetes is 32216, which is the allocated port for user vitorlucio, one of the 2 students working on this TP.

`cd client/`

run with `python main.py`

### URL to make requests to the client

The client has the endpoint `http://127.0.0.1:5000/callserver`, that will expect a POST request containing a json body like this:
```json
{
    "songs": ["Black Beatles", "Bounce Back"]
}
```
