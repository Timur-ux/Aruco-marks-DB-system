#!/bin/bash

docker compose down db
rm -r ./db/storage/
docker compose up -d db && docker compose logs db
