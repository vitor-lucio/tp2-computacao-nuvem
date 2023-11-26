# readme

## setup before running containers

`docker network create tp2-network`

both server and client folders should have a .env configured just like exemplo.env

## server

`cd server/`

`docker build . -t tp2-server --no-cache`

`docker run -p 32216:32216 --name tp2-server-container tp2-server`

### URL to make requests to server container

don't forget to send request with the expected body.

http://127.0.0.1:32216/api/recommend

## playlist-rules-generator
`cd playlist-rules-generator/`


`docker build . -t tp2-playlist-rules-generator --no-cache`


`docker run --name tp2-playlist-rules-generator-container tp2-playlist-rules-generator`

client's .env should have the server's container name in SERVER_NAME environment variable and server's port in SERVER_PORT.
