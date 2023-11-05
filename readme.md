# readme

## setup before running containers

docker network create tp2-network

both server and client folders should have a .env configured just like exemplo.env

## server

docker build . -t tp2-server --no-cache
docker run -p 30502:30502 --net tp2-network --name tp2-server-container tp2-server

### URL to make requests to server container

don't forget to send request with the expected body.

http://127.0.0.1:30502/api/recommend

## client

docker build . -t tp2-client --no-cache
docker run -p 30501:30501 --net tp2-network --name tp2-client-container tp2-client

### URL to make requests to client container

server container should be running and client's .env should have the server's container name in SERVER_NAME environment variable.
don't forget to send request with the expected body.

http://127.0.0.1:30501/