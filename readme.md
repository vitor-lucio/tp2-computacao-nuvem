# readme

## setup before running containers

docker network create tp2-network

both server and client folders should have a .env configured just like exemplo.env

## server

docker build . -t tp2-server --no-cache
docker run -p 32216:32216 --net tp2-network --name tp2-server-container tp2-server

### URL to make requests to server container

don't forget to send request with the expected body.

http://127.0.0.1:32216/api/recommend

## client

docker build . -t tp2-client --no-cache
docker run -p 37000:37000 --net tp2-network --name tp2-client-container tp2-client

### URL to make requests to client container

server container should be running and client's .env should have the server's container name in SERVER_NAME environment variable.
don't forget to send request with the expected body.

http://127.0.0.1:37000/api/recommender