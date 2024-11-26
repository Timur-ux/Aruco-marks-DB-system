#!/bin/bash

docker compose down backend
docker compose build backend
docker compose up -d backend
docker compose logs backend
