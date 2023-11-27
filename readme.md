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
