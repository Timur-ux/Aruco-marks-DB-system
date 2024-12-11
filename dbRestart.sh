#!/bin/bash

mkdir -p ./db/dumps
docker compose down postgres 
rm -r ./db/storage/
docker compose up -d postgres && docker compose logs postgres
